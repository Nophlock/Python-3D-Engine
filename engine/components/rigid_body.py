
from components import physics_component
from engine_math import vector3
from engine_math import quaternion
from engine_math import matrix3
from engine_math import matrix4

import math

class RigidBody(physics_component.PhysicsComponent):

    def __init__(self, col_shape):
        super().__init__(col_shape)

        self.mass = 1.0
        self.inv_mass = 1.0 / self.mass

        self.col_shape.calculate_intertia_tensor(self.mass)

        self.world_rotational_inertia = self.col_shape.get_inertia_tensor()
        self.inv_world_rotational_inertia = self.col_shape.get_inverse_inertia_tensor()

        self.local_centroid = self.col_shape.get_centroid()
        self.world_centroid = self.local_centroid

        self.linear_velocity = vector3.Vector3()
        self.angular_velocity = vector3.Vector3()

        self.force_accumulator = vector3.Vector3()
        self.torque_accumulator = vector3.Vector3()



    def get_name(self):
        return "RigidBody"

    def initialize(self):
        super().initialize()
        self.physics_engine = self.attached_entity.get_scene_manager().get_physics_engine()



    def apply_force(self, f, position):
        self.force_accumulator = self.force_accumulator + f
        self.torque_accumulator = self.torque_accumulator + (position - self.world_centroid).cross(f)

    def apply_central_force(self, force):
        self.apply_force(force, self.world_centroid)

    #updates our centroid based on our transform values
    def update_global_centroid_from_position(self):
        transform = self.attached_entity.transform
        rot = matrix3.Matrix3.from_matrix4(transform.get_local_rotation_matrix())
        self.world_centroid = rot.mul_vec3(self.local_centroid) + transform.get_local_position()

    #updates our transform based on our centroid value and orientation
    def update_position_from_global_centroid(self):
        transform = self.attached_entity.transform
        rot = matrix3.Matrix3.from_matrix4(transform.get_local_rotation_matrix())
        transform.set_local_position(rot.mul_vec3(self.local_centroid.negate()) + self.world_centroid)


    def fixed_update(self, dt):
        transform = self.attached_entity.transform

        #apply some gravity so we have something to see
        self.apply_central_force(self.attached_entity.scene_mgr.get_physics_engine().get_gravity() * self.mass)

        self.linear_velocity = self.linear_velocity + self.force_accumulator * self.inv_mass * dt
        self.angular_velocity = self.angular_velocity + self.inv_world_rotational_inertia.mul_vec3(self.torque_accumulator) * dt

        #reset force and torque so that an push doesnt happened forever
        self.force_accumulator = vector3.Vector3()
        self.torque_accumulator = vector3.Vector3()

        #integrate velocity
        self.world_centroid = self.world_centroid + self.linear_velocity * dt

        #integrate rotation
        spin = quaternion.Quaternion(self.angular_velocity, 0.0).mul_value(0.5) * transform.rotation
        new_rot = transform.rotation + spin.mul_value(dt)

        transform.set_local_rotation( new_rot.get_normalized() )
        self.update_position_from_global_centroid()

        rot_mat = matrix3.Matrix3.from_matrix4(transform.get_local_rotation_matrix())
        self.world_rotational_inertia = rot_mat * self.col_shape.get_inertia_tensor() * rot_mat.get_transpose()
        self.inv_world_rotational_inertia = self.world_rotational_inertia.get_inverse()




    #based on https://en.wikipedia.org/wiki/Collision_response#Impulse-Based_Reaction_Model
    def eval_collision(self, entity, col_points, normal, depth):

        #seperate object from the other one
        self.world_centroid = self.world_centroid - normal * depth

        #calulate impulse
        n = normal
        v = self.linear_velocity.negate() #v2 - v1 but for now only static collision

        #they going to resolve anyway
        if v.dot(n) > 0:
            return

        r1 = col_points[0] - self.world_centroid
        e = 0.5

        jr = (-(1.0+e)*v.dot(n)) / (self.inv_mass + (self.inv_world_rotational_inertia.mul_vec3(r1.cross(n)).cross(r1)).dot(n) )

        self.linear_velocity = self.linear_velocity - (n * jr * self.inv_mass)
        self.angular_velocity = self.angular_velocity - ( (self.inv_world_rotational_inertia.mul_vec3(r1.cross(n))) * jr)

        #friction calulation (static needs to be bigger than dynamic)
        jr_m = jr
        f_s = 1.0
        f_d = 0.8


        js = jr_m * f_s
        jd = jr_m * f_d

        t = (v - (n * n.dot(v)) ).get_normalized()
        jf = 0

        if v.dot(t) == 0 and v.dot(t)*self.mass < js:
            jf = -(v.dot(t) * self.mass)
        else:
            jf = -jd



        #self.linear_velocity = self.linear_velocity - (t * jf * self.inv_mass )
        #self.angular_velocity = self.angular_velocity - ( (self.inv_world_rotational_inertia.mul_vec3(r1.cross(t))) * jf)

        #self.update_position_from_global_centroid()



    def collision_started(self, collided_with):
        pass#self.attached_entity.get_component("MeshRenderer").get_materials()[0].assign_material("mesh_color", [1.0, 0.0, 0.0, 1.0])

    def collision_stopped(self, collided_with):
        pass#self.attached_entity.get_component("MeshRenderer").get_materials()[0].assign_material("mesh_color", [1.0, 1.0, 1.0, 1.0])


    def transform_was_modified(self, transform):
        super().transform_was_modified(transform)
        self.update_global_centroid_from_position()
