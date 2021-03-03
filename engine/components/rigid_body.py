
from components import physics_component
from engine_math import vector3
from engine_math import quaternion
from engine_math import matrix3

import math

class RigidBody(physics_component.PhysicsComponent):

    def __init__(self, col_shape):
        super().__init__(col_shape)


        #motion part
        self.center_of_mass = vector3.Vector3()
        self.momementum = vector3.Vector3()

        #dt
        self.velocity = vector3.Vector3()
        self.force = vector3.Vector3()

        self.mass = 1.0
        self.inv_mass = 1.0 / self.mass

        self.restitution = 0.5

        self.friction = 0.5
        self.dynamic_friction = 0.6

        #rotation part
        self.angular_velocity = vector3.Vector3()


        self.rotational_inertia = matrix3.Matrix3()
        self.inv_rotational_inertia = self.rotational_inertia

        #https://en.wikipedia.org/wiki/List_of_moments_of_inertia
        intertia_cube = (1.0 / 12.0) * self.mass * 2.0

        self.rotational_inertia.set_scale(intertia_cube, intertia_cube, intertia_cube)
        self.inv_rotational_inertia = self.rotational_inertia.get_inverse()

        #print(self.rotational_inertia * self.inv_rotational_inertia)


    def get_name(self):
        return "RigidBody"

    def initialize(self):
        super().initialize()
        self.physics_engine = self.attached_entity.get_scene_manager().get_physics_engine()



    def apply_force(self, f, position):
        self.force = f
        self.torque = f.cross(position - self.center_of_mass)



    def fixed_update(self, dt):
        transform = self.attached_entity.get_transform()

        #apply force (here we use gravity )
        self.force = self.force + self.physics_engine.get_gravity() * self.mass
        self.velocity = self.velocity + (self.force / self.mass) * dt

        #apply rotation

        angl_vel = self.rotational_inertia.mul_vec3(self.angular_velocity)
        spin = quaternion.Quaternion(angl_vel).mul_value(0.5) * transform.rotation


        new_pos = transform.get_local_position() + self.velocity * dt
        new_rot = transform.get_local_rotation() + spin.mul_value(dt)

        transform.set_local_position(new_pos)
        transform.set_local_rotation(new_rot.get_normalized() )

        self.force = vector3.Vector3()


    #based on https://en.wikipedia.org/wiki/Collision_response#Impulse-Based_Reaction_Model
    def eval_collision(self, entity, col_points, normal, depth):

        #seperate object from the other one
        n = normal.negate()
        self.attached_entity.get_transform().set_local_position(self.attached_entity.get_transform().get_local_position() + n * depth)


        #perform rigid body calculation
        v = vector3.Vector3() - self.velocity#is the relative velocity (since for now we use a static body, its only our own velocity)

        vel_along_normal = v.dot(n)

        if vel_along_normal < 0:#dont resolve if they are going to resolve anyway
            return

        r1 = col_points[0] - self.attached_entity.transform.get_local_position()
        r2 = col_points[1] - entity[0].transform.get_local_position()

        e = min(self.restitution , self.restitution )

        jr_u = -(1.0+e)*vel_along_normal
        jr_d = self.inv_mass + (self.inv_rotational_inertia.mul_vec3(r1.cross(n)).cross(r1) ).dot(n)
        jr = jr_u / jr_d


        self.velocity = self.velocity - (n * jr) * self.inv_mass
        self.angular_velocity = self.angular_velocity - self.inv_rotational_inertia.mul_vec3(r1.cross(n)) * jr


        #friction
        t = (v - normal * v.dot(normal)).get_normalized()
        jt_d = -(1.0+self.friction)*v.dot(t) / (self.inv_mass + (self.inv_rotational_inertia.mul_vec3(r1.cross(t)).cross(r1) ).dot(t) )



        #friction_impulse = vector3.Vector3()

        #if abs(jt_d) < jr_u * self.friction:
        #    friction_impulse = t * jt_d
        #else:
        #    friction_impulse = t * (-jr * self.friction)

        #self.velocity = self.velocity + friction_impulse * self.inv_mass
        #self.angular_velocity = self.angular_velocity + self.inv_rotational_inertia.mul_vec3(friction_impulse) * jt_d




    def collision_started(self, collided_with):
        pass#self.attached_entity.get_component("MeshRenderer").get_materials()[0].assign_material("mesh_color", [1.0, 0.0, 0.0, 1.0])

    def collision_stopped(self, collided_with):
        pass#self.attached_entity.get_component("MeshRenderer").get_materials()[0].assign_material("mesh_color", [1.0, 1.0, 1.0, 1.0])
