import math

from physics import gjk
from engine_math import vector3

#based on this article https://blog.winter.dev/2020/epa-algorithm/

#The algorithm tries to find the edge on the minkowski difference which is closest to the origin, if we have them, we calculate
#the normal of the edge. The main problem/task is to keep the simplex itself intact which means we cant randomly add vertices to our base tetrahedron
#(otherwise the normal of the edge would be incorrect) so we handle our tetrahedron as a mesh and keep adding
#points respectively until we find the closest edge on the minkowski difference
class EPA:

    #calculate the normals of all faces of the polygon(not a tetrahedron anymore) and returns the index of the vertex which is closest to the origin
    @staticmethod
    def get_face_normals(simplex_points, faces):

        normals = []
        min_triangle = 0
        min_distance = math.inf

        for i in range(0, len(faces), 3):
            a = simplex_points[ faces[i  ] ]
            b = simplex_points[ faces[i+1] ]
            c = simplex_points[ faces[i+2] ]

            normal = (b-a).cross(c-a).get_normalized()

            distance = normal.dot(a)

            if distance < 0:
                normal = normal.negate()
                distance = -distance

            normals.append([normal, distance])

            if distance < min_distance:
                min_triangle = i // 3
                min_distance = distance


        return normals, min_triangle


    @staticmethod
    def add_if_unique_edge(edges, faces, a, b):

        reverse = -1

        for i in range(len(edges)):

            if edges[i][0] == faces[b] and edges[i][1] == faces[a]:
                reverse = i
                break

        if reverse != len(edges) - 1:
            del edges[reverse]

        edges.append([faces[a], faces[b]] )

        return edges

    @staticmethod
    def get_penetration_data(simplex_points, polygon_a, polygon_b):

        min_distance = math.inf
        min_normal = vector3.Vector3()

        faces = [   0, 1, 2,
                    0, 3, 1,
                    0, 2, 3,
                    1, 3, 2 ]

        normals, min_face = EPA.get_face_normals(simplex_points, faces)

        while min_distance == math.inf:

            min_normal = normals[min_face][0]
            min_distance = normals[min_face][1]

            support = gjk.GJK.support_function(polygon_a, polygon_b, min_normal)
            s_distance = min_normal.dot(support)

            if abs(s_distance - min_distance) > 0.001:
                min_distance = math.inf

                unique_edges = []
                i = 0

                while i < len(normals):

                    if gjk.GJK.is_same_direction(normals[i][0], support):
                        f = i * 3

                        unique_edges = EPA.add_if_unique_edge(unique_edges, faces, f  , f+1)
                        unique_edges = EPA.add_if_unique_edge(unique_edges, faces, f+1, f+2)
                        unique_edges = EPA.add_if_unique_edge(unique_edges, faces, f+2, f  )

                        faces[f + 2] = faces[-1]; faces.pop()
                        faces[f + 1] = faces[-1]; faces.pop()
                        faces[f    ] = faces[-1]; faces.pop()

                        normals[i] = normals[-1]; normals.pop()
                        i = i - 1

                    i = i + 1


                new_faces = []

                for i in range(len(unique_edges)):
                    new_faces.append(unique_edges[i][0])
                    new_faces.append(unique_edges[i][1])
                    new_faces.append(len(simplex_points) )

                simplex_points.append(support)
                new_normals, new_min_face = EPA.get_face_normals(simplex_points, new_faces)

                old_min_distance = math.inf
                min_face = 0

                for i in range(len(normals)):
                    if normals[i][1] < old_min_distance:
                        old_min_distance = normals[i][1]
                        min_face = i

                if new_normals[new_min_face][1] < old_min_distance:
                    min_face = new_min_face + len(normals)

                faces.extend(new_faces)
                normals.extend(new_normals)


        #add a small amount to it, to avoid jiterring and another collision in the next frame
        return min_normal, min_distance + 0.00001
