
import math

from vector3 import Vector3
from matrix4 import Matrix4

class AABB:

    def __init__(self, min = Vector3(), max = Vector3(), calc_knots = False ):
        self.min = min
        self.max = max

        self.unprojected = {}
        self.unprojected["min"] = min
        self.unprojected["max"] = max
        self.unprojected["cached_transform"] = None
        self.unprojected["modified_stamp"] = -1
        self.unprojected["knots"] = []

        if calc_knots:
            self.calculate_knots()

    def get_min_max(self):
        return self.min, self.max

    def set_min_max(self, min, max):
        self.min = min
        self.max = max

        self.unprojected["min"] = min
        self.unprojected["max"] = max
        self.unprojected["modified_stamp"] = self.unprojected["modified_stamp"] + 1

        self.calculate_knots()


    def get_knots(self):
        return self.unprojected["knots"]

    def calculate_knots(self):

        min = self.min
        max = self.max

        self.unprojected["knots"].append(Vector3(min.x, min.y, min.z)) #000
        self.unprojected["knots"].append(Vector3(min.x, min.y, max.z)) #001
        self.unprojected["knots"].append(Vector3(min.x, max.y, min.z)) #010
        self.unprojected["knots"].append(Vector3(min.x, max.y, max.z)) #011
        self.unprojected["knots"].append(Vector3(max.x, min.y, min.z)) #100
        self.unprojected["knots"].append(Vector3(max.x, min.y, max.z)) #101
        self.unprojected["knots"].append(Vector3(max.x, max.y, min.z)) #110
        self.unprojected["knots"].append(Vector3(max.x, max.y, max.z)) #111



    #see for basic ray aabb intersection https://gamedev.stackexchange.com/questions/18436/most-efficient-aabb-vs-ray-collision-algorithms
    def intersect_ray(self, ray_start, ray_dir, a_min, a_max):

        dir_frac_x = 1.0
        dir_frac_y = 1.0
        dir_frac_z = 1.0

        if ray_dir.x != 0: dir_frac_x = 1.0 / ray_dir.x
        if ray_dir.y != 0: dir_frac_y = 1.0 / ray_dir.y
        if ray_dir.z != 0: dir_frac_z = 1.0 / ray_dir.z

        t1 = (a_min.x - ray_start.x) * dir_frac_x
        t2 = (a_max.x - ray_start.x) * dir_frac_x

        t3 = (a_min.y - ray_start.y) * dir_frac_y
        t4 = (a_max.y - ray_start.y) * dir_frac_y

        t5 = (a_min.z - ray_start.z) * dir_frac_z
        t6 = (a_max.z - ray_start.z) * dir_frac_z


        t_min = max(max(min(t1, t2), min(t3, t4)), min(t5, t6))
        t_max = min(min(max(t1, t2), max(t3, t4)), max(t5, t6))

        if t_max < 0:
            return False, -1, -1

        if t_min > t_max:
            return False, -1, -1

        return True, t_min, t_max


    #note that this is not 100% acurrate but its the best method comparing performance to accuracy
    #the accurate method would be to transform every vertex in the cpu and then make the min-max check
    def calculate_aabb_unprojected(self):

        matrix = self.unprojected["cached_transform"].get_transformation_matrix()


        u_min = Vector3(math.inf, math.inf, math.inf)
        u_max = Vector3(-math.inf, -math.inf,-math.inf)


        for i in range(len(self.unprojected["knots"])):
            t_vec = matrix.mul_vec3( self.unprojected["knots"][i] )

            u_min.x = min(t_vec.x, u_min.x)
            u_min.y = min(t_vec.y, u_min.y)
            u_min.z = min(t_vec.z, u_min.z)

            u_max.x = max(t_vec.x, u_max.x)
            u_max.y = max(t_vec.y, u_max.y)
            u_max.z = max(t_vec.z, u_max.z)

        self.unprojected["min"] = u_min
        self.unprojected["max"] = u_max


    def check_unprojection_min_max_update(self, transform):

        #just check if the stored transform was updated
        if transform == None:

            if self.unprojected["cached_transform"] != None and self.unprojected["modified_stamp"] != self.unprojected["cached_transform"].get_modified_stamp():
                self.unprojected["modified_stamp"] = self.unprojected["cached_transform"].get_modified_stamp()

                self.calculate_aabb_unprojected()

                return True
        else:

            if self.unprojected["cached_transform"] != transform or self.unprojected["modified_stamp"] != transform.get_modified_stamp():
                self.unprojected["cached_transform"] = transform
                self.unprojected["modified_stamp"] = transform.get_modified_stamp()

                self.calculate_aabb_unprojected()

                return True

        return False

    def intersect_aabb_ray(self, transform, ray_start, ray_dir):
        self.check_unprojection_min_max_update(transform)
        return self.intersect_ray(ray_start, ray_dir, self.unprojected["min"], self.unprojected["max"])



    #treats the aabb as on obb
    def intersect_obb_ray(self, transform, ray_start, ray_dir):


        rot_mat = transform.rotation_matrix.get_transpose()#the transpose of a rotation matrix is the inverse

        inv_start = ray_start - transform.position
        inv_start = rot_mat.mul_vec3(inv_start)

        inv_dir = rot_mat.mul_vec3(ray_dir)

        return self.intersect_ray(inv_start, inv_dir, self.min, self.max)

    def get_modified_timestamp(self):
        return self.unprojected["modified_stamp"]

    def __repr__(self):
        result = "MIN:\n"
        result = result + str(self.min)
        result = result + "MAX:\n"
        result = result + str(self.max)

        return result
