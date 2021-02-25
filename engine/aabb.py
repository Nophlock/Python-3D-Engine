
import math

from engine_math import vector3

class AABB:

    def __init__(self, min = vector3.Vector3(), max = vector3.Vector3(), calc_knots = False ):
        self.min = min
        self.max = max

        self.unprojected = {}
        self.unprojected["min"] = min
        self.unprojected["max"] = max
        self.unprojected["base_knots"] = []
        self.unprojected["transformed_knots"] = []

        if calc_knots:
            self.calculate_knots("base_knots", min, max)
            self.unprojected["transformed_knots"] = self.unprojected["base_knots"]#at the beginning they should be the same

    def get_min_max(self):
        return self.min, self.max

    def get_unprojected_min_max(self):
        return self.unprojected["min"], self.unprojected["max"]

    def set_min_max(self, min, max):
        self.min = min
        self.max = max

        self.unprojected["min"] = min
        self.unprojected["max"] = max
        self.unprojected["modified_stamp"] = self.unprojected["modified_stamp"] + 1

        self.calculate_knots("base_knots", min, max)


    def get_base_knots(self):
        return self.unprojected["base_knots"]

    def get_transformed_knots(self):
        return self.unprojected["transformed_knots"]


    def calculate_transformed_knots(self):
        return self.calculate_knots("transformed_knots", self.unprojected["min"], self.unprojected["max"])

    def calculate_base_knots(self):
        self.calculate_knots("base_knots", self.min, self.max)

    def calculate_knots(self, index, min, max):

        self.unprojected[index] = []
        self.unprojected[index].append(vector3.Vector3(min.x, min.y, min.z)) #000
        self.unprojected[index].append(vector3.Vector3(min.x, min.y, max.z)) #001
        self.unprojected[index].append(vector3.Vector3(min.x, max.y, min.z)) #010
        self.unprojected[index].append(vector3.Vector3(min.x, max.y, max.z)) #011
        self.unprojected[index].append(vector3.Vector3(max.x, min.y, min.z)) #100
        self.unprojected[index].append(vector3.Vector3(max.x, min.y, max.z)) #101
        self.unprojected[index].append(vector3.Vector3(max.x, max.y, min.z)) #110
        self.unprojected[index].append(vector3.Vector3(max.x, max.y, max.z)) #111



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
    def calculate_aabb_unprojected(self, transform):

        matrix = transform.get_transformation_matrix()


        u_min = vector3.Vector3(math.inf, math.inf, math.inf)
        u_max = vector3.Vector3(-math.inf, -math.inf,-math.inf)


        for i in range(len(self.unprojected["base_knots"])):
            t_vec = matrix.mul_vec3( self.unprojected["base_knots"][i] )

            u_min.x = min(t_vec.x, u_min.x)
            u_min.y = min(t_vec.y, u_min.y)
            u_min.z = min(t_vec.z, u_min.z)

            u_max.x = max(t_vec.x, u_max.x)
            u_max.y = max(t_vec.y, u_max.y)
            u_max.z = max(t_vec.z, u_max.z)

        self.unprojected["min"] = u_min
        self.unprojected["max"] = u_max
        self.calculate_knots("transformed_knots", u_min, u_max)


    def intersect_aabb_ray(self, transform, ray_start, ray_dir):
        return self.intersect_ray(ray_start, ray_dir, self.unprojected["min"], self.unprojected["max"])



    #treats the aabb as on obb
    def intersect_obb_ray(self, transform, ray_start, ray_dir):


        rot_mat = transform.rotation_matrix.get_transpose()#the transpose of a rotation matrix is the inverse

        inv_start = ray_start - transform.position
        inv_start = rot_mat.mul_vec3(inv_start)

        inv_dir = rot_mat.mul_vec3(ray_dir)

        return self.intersect_ray(inv_start, inv_dir, self.min, self.max)

    def __repr__(self):
        result = "MIN:\n"
        result = result + str(self.min)
        result = result + "MAX:\n"
        result = result + str(self.max)

        return result
