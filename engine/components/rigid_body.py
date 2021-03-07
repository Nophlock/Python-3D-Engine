
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

        self.damping = 1.0
        self.friction = 0.05

        self.col_shape.calculate_inertia_tensor(self.mass)

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

        #if self.force_accumulator.get_len() > 0.1:
        #    self.awake = True

    def apply_central_force(self, force):
        self.apply_force(force, self.world_centroid)

    def get_point_velocity(self, point):
        return self.linear_velocity + (self.angular_velocity.cross(point - self.world_centroid))

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


    def integrate(self, dt):

        if self.awake == False:
            return
        elif self.inv_mass == 0.0:
            return

        transform = self.attached_entity.transform

        self.linear_velocity = self.linear_velocity + self.force_accumulator * self.inv_mass * dt
        self.angular_velocity = self.angular_velocity + self.inv_world_rotational_inertia.mul_vec3(self.torque_accumulator) * dt

        #integrate velocity
        self.world_centroid = self.world_centroid + self.linear_velocity * dt


    def update_positions(self, dt):

        if self.awake == False:
            return

        transform = self.attached_entity.transform
        #integrate rotation
        spin = quaternion.Quaternion(self.angular_velocity, 0.0).mul_value(0.5) * transform.rotation
        new_rot = transform.rotation + spin.mul_value(dt)

        self.update_position_from_global_centroid()
        transform.set_local_rotation( new_rot.get_normalized() )

        #reset force and torque so that an push doesnt happened forever
        self.force_accumulator = vector3.Vector3()
        self.torque_accumulator = vector3.Vector3()



    #based on https://en.wikipedia.org/wiki/Collision_response#Impulse-Based_Reaction_Model
    def eval_collision(self, entity, collision_data, dt):

        #calulate impact impulse
        n = collision_data["min_normal"]
        v = self.get_point_velocity( collision_data["contact_points"][0] ).negate()
        vrel = n.dot(v)
        threshold = 0.01

        if vrel > 0.0:
            return

        r1 = collision_data["contact_points"][0] - self.world_centroid
        e = 0.4#coefficient for wood
        allow_penetration = 0.01#taken from box2d lite
        bias_factor = 0.2

        bias_velocity = -(bias_factor / dt) * min(0.0, -collision_data["min_distance"] + allow_penetration)


        numerator = -(1.0+e)*vrel + bias_velocity
        denominator = self.inv_mass + (self.inv_world_rotational_inertia.mul_vec3(r1.cross(n)).cross(r1)).dot(n)

        j = (numerator / denominator) * collision_data["force_distribution"]
        j = max(j, 0.0)

        force = n * j

        self.linear_velocity = self.linear_velocity - (force * self.inv_mass)
        self.angular_velocity = self.angular_velocity - ( self.inv_world_rotational_inertia.mul_vec3(r1.cross(force)))

        #friction calulation
        t = (v - (n * v.dot(n)) ).get_normalized()

        numerator = -t.dot(v)
        denomniator = self.inv_mass + (self.inv_world_rotational_inertia.mul_vec3(r1.cross(t)).cross(r1)).dot(t)

        jt = (numerator / denominator) * collision_data["force_distribution"]


        max_impulse = j * self.friction
        jt = max(-max_impulse, min(jt, max_impulse))#normaly clamp(jt, -max_impulse, max_impulse)

        tan_force = t * jt

        self.linear_velocity = self.linear_velocity - (tan_force * self.inv_mass)
        self.angular_velocity = self.angular_velocity - ( self.inv_world_rotational_inertia.mul_vec3(r1.cross(tan_force)))



        #self.linear_velocity = self.linear_velocity - (t * jf * self.inv_mass )
        #self.angular_velocity = self.angular_velocity - ( (self.inv_world_rotational_inertia.mul_vec3(r1.cross(t))) * jf)

        #self.update_position_from_global_centroid()


    def transform_was_modified(self, transform):
        super().transform_was_modified(transform)
        self.update_global_centroid_from_position()

        #at some point we should just use the tranpose of the rot matrix for performace
        rot_mat = matrix3.Matrix3.from_matrix4(transform.get_local_rotation_matrix())
        self.world_rotational_inertia = rot_mat * self.col_shape.get_inertia_tensor() * rot_mat.get_inverse()
        self.inv_world_rotational_inertia = self.world_rotational_inertia.get_inverse()
