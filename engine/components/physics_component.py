
from components import component

class PhysicsComponent(component.Component):

    def __init__(self, col_shape):
        self.col_shape = col_shape
        self.awake = True

    def get_name(self):
        return "PhysicsComponent"

    def set_awake(self, a):
        self.awake = a

    def is_awake(self):
        return self.awake

    def initialize(self):
        self.attached_entity.get_scene_manager().get_physics_engine().add_physics_object(self.attached_entity, self)

    #for now we use the aabb from the MeshRenderer for that which is technicly wrong, but for now its fine
    def get_collision_aabb(self):
        return self.attached_entity.get_component("MeshRenderer").get_aabb()

    def get_collision_polygon(self):
        return self.col_shape.get_transformed_points()

    def get_center_of_mass(self):
        return self.attached_entity.get_component("MeshRenderer").get_meshes()[0].get_informations()["center_of_mass"]


    def eval_collision(self, entity, collision_data):
        pass

    def collision_started(self, col_data):
        pass

    def collision_stopped(self):
        pass

    def transform_was_modified(self, transform):
        self.col_shape.transform_was_changed(transform)
