

from physics import collision_shape
from engine_math import vector3
from engine_math import matrix3

class BoxCollisionShape(collision_shape.CollisionShape):

    def __init__(self, w, h, d):
        super().__init__()

        h_w = w * 0.5
        h_h = h * 0.5
        h_d = d * 0.5


        self.collision_base_points.append(vector3.Vector3(-h_w, -h_h, -h_d)) #000
        self.collision_base_points.append(vector3.Vector3(-h_w, -h_h, h_d)) #001
        self.collision_base_points.append(vector3.Vector3(-h_w, h_h, -h_d)) #010
        self.collision_base_points.append(vector3.Vector3(-h_w, h_h, h_d)) #011

        self.collision_base_points.append(vector3.Vector3(h_w, -h_h, -h_d)) #100
        self.collision_base_points.append(vector3.Vector3(h_w, -h_h, h_d)) #101
        self.collision_base_points.append(vector3.Vector3(h_w, h_h, -h_d)) #110
        self.collision_base_points.append(vector3.Vector3(h_w, h_h, h_d)) #111

        self.transformed_collision_points = self.collision_base_points

    def calculate_intertia_tensor(self, mass):

        self.inertia_tensor = matrix3.Matrix3()
        intertia_cube = (1.0 / 12.0) * mass * 2.0

        self.inertia_tensor.set_scale(intertia_cube, intertia_cube, intertia_cube)
        self.inv_inertia_tensor = self.inertia_tensor.get_inverse()
