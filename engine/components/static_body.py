
from components import physics_component

class StaticBody(physics_component.PhysicsComponent):

    def __init__(self, col_shape):
        super().__init__(col_shape)

    def get_name(self):
        return "StaticBody"


    def eval_collision(self, entity, col_points, normal, depth):
        pass

    def collision_started(self, collided_with):
        pass#self.attached_entity.get_component("MeshRenderer").get_materials()[0].assign_material("mesh_color", [1.0, 0.0, 0.0, 1.0])

    def collision_stopped(self, collided_with):
        pass#self.attached_entity.get_component("MeshRenderer").get_materials()[0].assign_material("mesh_color", [1.0, 1.0, 1.0, 1.0])
