
from components import physics_component

class StaticBody(physics_component.PhysicsComponent):

    def __init__(self, col_shape):
        super().__init__(col_shape)

    def get_name(self):
        return "StaticBody"
