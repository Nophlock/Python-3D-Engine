
from engine_math import vector3

class GJK:

    @staticmethod
    def get_furthest_point(polygon_list, direction):
        furthest = polygon_list[0]
        distance = furthest.dot( direction )
        index = 0

        for i in range(1, len(polygon_list)):
            _dst = polygon_list[i].dot(direction)

            if _dst > distance:
                distance = _dst
                furthest = polygon_list[i]
                index = i

        return furthest, index

    @staticmethod
    def support_function(polygon_a, polygon_b, direction):
        point_a, poly_ai = GJK.get_furthest_point(polygon_a, direction)
        point_b, poly_bi = GJK.get_furthest_point(polygon_b, direction.negate())

        return [point_a - point_b, poly_ai, poly_bi]

    @staticmethod
    def is_same_direction(vec_a, vec_b):
        return vec_b.dot(vec_a) > 0

    @staticmethod
    def is_polygon_colliding(polygon_a, polygon_b):

        simplex_points = [GJK.support_function(polygon_a, polygon_b, vector3.Vector3.unit_x())]
        c_dir = simplex_points[0][0].negate()

        r = False

        while r == False:
            support = GJK.support_function(polygon_a, polygon_b, c_dir)

            if support[0].dot(c_dir) <= 0:
                return False, None

            simplex_points.insert(0, support)
            point_count = len(simplex_points)

            if point_count == 2:
                r, simplex_points, c_dir = GJK.line_check(simplex_points, c_dir)
            elif point_count == 3:
                r, simplex_points, c_dir = GJK.triangle_check(simplex_points, c_dir)
            elif point_count == 4:
                r, simplex_points, c_dir = GJK.tetrahedron_check(simplex_points, c_dir)


        return True, simplex_points




    @staticmethod
    def line_check(simplex, c_dir):
        a = simplex[0]
        b = simplex[1]

        ab = b[0] - a[0]
        a0 = a[0].negate()

        if GJK.is_same_direction(ab, a0):
            return False, simplex, ab.cross(a0).cross(ab)

        return False, [a], a0


    def triangle_check(simplex, c_dir):
        a = simplex[0]
        b = simplex[1]
        c = simplex[2]

        ab = b[0] - a[0]
        ac = c[0] - a[0]
        a0 = a[0].negate()

        abc = ab.cross(ac)

        if GJK.is_same_direction(abc.cross(ac), a0):
            if GJK.is_same_direction(ac, a0):
                return False, [a,c], ac.cross(a0).cross(ac)
            else:
                return GJK.line_check([a,b], c_dir)
        else:

            if GJK.is_same_direction(ab.cross(abc), a0):
                return GJK.line_check([a,b], c_dir)
            else:
                if GJK.is_same_direction(abc, a0):
                    return False, simplex, abc
                else:
                    return False, [a,c,b], abc.negate()



    def tetrahedron_check(simplex, c_dir):
        a = simplex[0]
        b = simplex[1]
        c = simplex[2]
        d = simplex[3]

        ab = b[0] - a[0]
        ac = c[0] - a[0]
        ad = d[0] - a[0]
        a0 = a[0].negate()

        abc = ab.cross(ac)
        acd = ac.cross(ad)
        adb = ad.cross(ab)

        if GJK.is_same_direction(abc, a0):
            return GJK.triangle_check([a,b,c], c_dir)

        if GJK.is_same_direction(acd, a0):
            return GJK.triangle_check([a,c,d], c_dir)

        if GJK.is_same_direction(adb, a0):
            return GJK.triangle_check([a,d,b], c_dir)


        return True, simplex, c_dir
