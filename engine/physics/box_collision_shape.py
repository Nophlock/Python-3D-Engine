

from physics import collision_shape
from engine_math import vector3

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
