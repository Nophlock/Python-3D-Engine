
from components import component

class PhysicsComponent(component.Component):

    def get_name(self):
        return "PhysicsComponent"

    def initialize(self):
        self.attached_entity.get_scene_manager().get_physics_engine().add_physics_object(self.attached_entity, self)

    #for now we use the aabb from the MeshRenderer for that which is technicly wrong, but for now its fine
    def get_collision_aabb(self):
        return self.attached_entity.get_component("MeshRenderer").get_aabb()

    def get_collision_polygon(self):

        return self.get_collision_aabb().get_transformed_knots()


    def eval_collision(self, collided_with, normal, depth):
        pass

    def collision_started(self, collided_with):
        pass

    def collision_stopped(self, collided_with):
        pass
