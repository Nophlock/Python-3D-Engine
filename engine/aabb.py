
from vector3 import Vector3
from matrix4 import Matrix4

class AABB:

    def __init__(self, min = Vector3(), max = Vector3() ):
        self.min = min
        self.max = max


    #see for basic ray aabb intersection https://www.scratchapixel.com/lessons/3d-basic-rendering/minimal-ray-tracer-rendering-simple-shapes/ray-box-intersection
    #TODO: shorten the code / make it less performance hungry
    def intersect_ray(self, transform, ray_start, ray_dir):


        pos_mat = Matrix4()
        pos_mat.set_translation(-transform.position.x, -transform.position.y, -transform.position.z) #the inverse of a position matrix is just the negation of the translation part
        rot_mat = transform.rotation_matrix.get_transpose()#the transpose of a rotation matrix is the inverse

        inv_start = pos_mat.mul_vec3(ray_start)
        inv_start = rot_mat.mul_vec3(inv_start)

        inv_dir = rot_mat.mul_vec3(ray_dir)

        t_min = (self.min.x - inv_start.x) / inv_dir.x
        t_max = (self.max.x - inv_start.x) / inv_dir.x

        if t_min > t_max:
            t_min, t_max = (t_max, t_min)

        ty_min = (self.min.y - inv_start.y) / inv_dir.y
        ty_max = (self.max.y - inv_start.y) / inv_dir.y

        if ty_min > ty_max:
            ty_min, ty_max = (ty_max, ty_min)

        if t_min > ty_max or ty_min > t_max:
            return False, -1, -1

        if ty_min > t_min:
            t_min = ty_min

        if ty_max < t_max:
            t_max = ty_max

        tz_min = (self.min.z - inv_start.z) / inv_dir.z
        tz_max = (self.max.z - inv_start.z) / inv_dir.z

        if tz_min > tz_max:
            tz_min, tz_max = (tz_max, tz_min)

        if t_min > tz_max or tz_min > t_max:
            return False, -1, -1

        if tz_min > t_min:
            t_min = tz_min

        if tz_max < t_max:
            t_max = tz_max


        return True, t_min, t_max

    def __repr__(self):
        result = "MIN:\n"
        result = result + str(self.min)
        result = result + "MAX:\n"
        result = result + str(self.max)

        return result
