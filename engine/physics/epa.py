import math
import sys

from physics import gjk
from engine_math import vector3

#based on this article https://blog.winter.dev/2020/epa-algorithm/

#The algorithm tries to find the edge on the minkowski difference which is closest to the origin, if we have them, we calculate
#the normal of the edge. The main problem/task is to keep the simplex itself intact which means we cant randomly add vertices to our base tetrahedron
#(otherwise the normal of the edge would be incorrect) so we handle our tetrahedron as a mesh and keep adding
#points respectively until we find the closest edge on the minkowski difference

VECTOR = 0
A_INDX = 1
B_INDX = 2

EPA_TOLERANCE = 0.0001
EPA_MAX_NUM_LOOSE_EDGES = 32
EPA_MAX_NUM_FACES = 64
EPA_MAX_NUM_ITERATIONS = 64

class EPA:

    #https://gamedev.stackexchange.com/questions/23743/whats-the-most-efficient-way-to-find-barycentric-coordinates
    @staticmethod
    def barycentric(p,n, a, b, c):
        a_abc = n.dot( (b-a).cross(c-a))
        a_pbc = n.dot( (b-p).cross(c-p))
        a_pca = n.dot( (c-p).cross(a-p))

        if a_abc == 0.0:
            a_abc = 1.0

        v = a_pbc / a_abc
        w = a_pca / a_abc
        u = 1.0 - v - w

        return v,w,u

    #based on https://github.com/kevinmoran/GJK/blob/master/GJK.h#L172 since his algorithm seems more robust then the other(or i implemented the other one wrong)
    @staticmethod
    def get_penetration_data(simplex_points, polygon_a,mat_a, polygon_b, mat_b):

        a = simplex_points[0]
        b = simplex_points[1]
        c = simplex_points[2]
        d = simplex_points[3]

        faces = []

        for i in range(EPA_MAX_NUM_FACES):
            pack = [ a,b,c, vector3.Vector3() ]

            faces.append( pack )



        faces[0] = [a,b,c,(b[VECTOR]-a[VECTOR]).cross(c[VECTOR]-a[VECTOR]).get_normalized()]#abc
        faces[1] = [a,c,d,(c[VECTOR]-a[VECTOR]).cross(d[VECTOR]-a[VECTOR]).get_normalized()]#acd
        faces[2] = [a,d,b,(d[VECTOR]-a[VECTOR]).cross(b[VECTOR]-a[VECTOR]).get_normalized()]#adb
        faces[3] = [b,d,c,(d[VECTOR]-b[VECTOR]).cross(c[VECTOR]-b[VECTOR]).get_normalized()]#bdc

        num_faces = 4
        closest_face = 0

        for iteration in range(EPA_MAX_NUM_ITERATIONS):

            min_dist = faces[0][0][VECTOR].dot(faces[0][3])
            closest_face = 0

            for i in range(1, num_faces):
                dist = faces[i][0][VECTOR].dot(faces[i][3])

                if dist < min_dist:
                    min_dist = dist
                    closest_face = i

            search_dir = faces[closest_face][3]
            p = gjk.GJK.support_function(polygon_a, polygon_b, search_dir)

            if p[VECTOR].dot(search_dir) - min_dist < EPA_TOLERANCE:
                break

            loose_edges = []
            for i in range(EPA_MAX_NUM_LOOSE_EDGES):
                loose_edges.append([0,0])

            num_loose_edges = 0
            i = 0

            while i < num_faces:

                if faces[i][3].dot(p[VECTOR] - faces[i][0][VECTOR]) > 0:

                    for j in range(3):

                        current_edge = [faces[i][j], faces[i][(j+1)%3]]
                        found_edge = False
                        k = 0

                        while k < num_loose_edges:

                            if loose_edges[k][1] == current_edge[0] and loose_edges[k][0] == current_edge[1]:
                                loose_edges[k][0] = loose_edges[num_loose_edges-1][0]
                                loose_edges[k][1] = loose_edges[num_loose_edges-1][1]
                                num_loose_edges = num_loose_edges - 1

                                found_edge = True
                                k = num_loose_edges

                            k = k + 1

                        if not found_edge:

                            if num_loose_edges >= EPA_MAX_NUM_LOOSE_EDGES:
                                break

                            loose_edges[num_loose_edges][0] = current_edge[0]
                            loose_edges[num_loose_edges][1] = current_edge[1]
                            num_loose_edges = num_loose_edges + 1


                    faces[i][0] = faces[num_faces-1][0]
                    faces[i][1] = faces[num_faces-1][1]
                    faces[i][2] = faces[num_faces-1][2]
                    faces[i][3] = faces[num_faces-1][3]

                    num_faces = num_faces - 1
                    i = i - 1

                i = i + 1

            for i in range(num_loose_edges):

                if num_faces >= EPA_MAX_NUM_FACES:
                    break

                faces[num_faces][0] = loose_edges[i][0]
                faces[num_faces][1] = loose_edges[i][1]
                faces[num_faces][2] = p
                faces[num_faces][3] = (loose_edges[i][0][VECTOR]-loose_edges[i][1][VECTOR]).cross(loose_edges[i][0][VECTOR]-p[VECTOR]).get_normalized()

                if faces[num_faces][0][VECTOR].dot(faces[num_faces][3]) + EPA_TOLERANCE < 0:
                    tmp = faces[num_faces][0]

                    faces[num_faces][0] = faces[num_faces][1]
                    faces[num_faces][1] = tmp
                    faces[num_faces][3] = faces[num_faces][3].negate()

                num_faces = num_faces + 1


        if iteration >= EPA_MAX_NUM_ITERATIONS:
            print("warning, epa couldnt find the closes triangle point")

        min_normal = search_dir
        min_distance = min_normal.dot(p[VECTOR])

        contact_points = []
        local_contact_points = []

        point_on_closest_triangle = min_normal * min_distance
        closest_triangle_a = faces[closest_face][0][VECTOR]
        closest_triangle_b = faces[closest_face][1][VECTOR]
        closest_triangle_c = faces[closest_face][2][VECTOR]

        v,w,u = EPA.barycentric(point_on_closest_triangle,min_normal, closest_triangle_a, closest_triangle_b, closest_triangle_c)

        polygon_triangle_a_0 = polygon_a[ faces[closest_face][0][1] ]
        polygon_triangle_a_1 = polygon_a[ faces[closest_face][1][1] ]
        polygon_triangle_a_2 = polygon_a[ faces[closest_face][2][1] ]

        polygon_triangle_b_0 = polygon_b[ faces[closest_face][0][2] ]
        polygon_triangle_b_1 = polygon_b[ faces[closest_face][1][2] ]
        polygon_triangle_b_2 = polygon_b[ faces[closest_face][2][2] ]

        contact_point_a = polygon_triangle_a_0 * v + polygon_triangle_a_1 * w + polygon_triangle_a_2 * u
        contact_point_b = polygon_triangle_b_0 * v + polygon_triangle_b_1 * w + polygon_triangle_b_2 * u

        #note that our contact points should be inside of the mesh not on top of them
        contact_points.append(contact_point_a - min_normal * min_distance)
        contact_points.append(contact_point_b)

        local_contact_points.append(mat_a.get_inverse().mul_vec3(contact_point_a))
        local_contact_points.append(mat_b.get_inverse().mul_vec3(contact_point_b))

        #based on http://allenchou.net/2013/12/game-physics-contact-generation-epa/
        if min_normal.x >= 0.57735:
            t = vector3.Vector3(min_normal.y, -min_normal.x, 0.0)
        else:
            t = vector3.Vector3(0.0, min_normal.z, -min_normal.y)

        t1 = t.get_normalized()
        t2 = min_normal.cross(t1)

        data = {}
        data["contact_points"] = contact_points
        data["local_contact_points"] = local_contact_points
        data["tangents"] = [t1, t2]
        data["min_normal"] = min_normal
        data["min_distance"] = min_distance
        data["seperation_point"] = min_normal * min_distance


        return data
