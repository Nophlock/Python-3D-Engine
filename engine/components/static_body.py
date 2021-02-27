
from components import physics_component

class StaticBody(physics_component.PhysicsComponent):

    def __init__(self):
        super().__init__()

    def get_name(self):
        return "StaticBody"


    #this is just for testing for now, since static bodies dont move and so this behavior here is not wanted
    def eval_collision(self, collided_with, normal, depth):
        self.attached_entity.get_transform().set_local_position(self.attached_entity.get_transform().get_local_position() + normal * -depth)

    def collision_started(self, collided_with):
        self.attached_entity.get_component("MeshRenderer").get_materials()[0].assign_material("mesh_color", [1.0, 0.0, 0.0, 1.0])

    def collision_stopped(self, collided_with):
        self.attached_entity.get_component("MeshRenderer").get_materials()[0].assign_material("mesh_color", [1.0, 1.0, 1.0, 1.0])
