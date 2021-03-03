


from components import component
from aabb import AABB
from material import Material
from engine_math import matrix4
from debug_shapes import DebugShapes
from mesh import Mesh

from pyglet.gl 		import *


class PrimitiveRender(component.Component):

    def __init__(self, primitive_mesh):
        super().__init__()

        self.material = Material()
        self.primitive = primitive_mesh

        self.material.assign_material("mesh_color", [1.0, 1.0, 1.0, 1.0])

    def get_name(self):
        return "PrimitiveRender"

    def render(self, camera, shader):

        shader.send_matrix_4 (shader.get_location("transformation_matrix") , self.attached_entity.get_transform().get_transformation_matrix())
        shader.send_integer(shader.get_location("has_animation"), 0)

        #glPolygonMode(GL_FRONT_AND_BACK,GL_LINE);

        shader.prepare_render(self.primitive, self.material)
        self.primitive.render()
        shader.unprepare_render(self.primitive, self.material)

        #glPolygonMode(GL_FRONT_AND_BACK,GL_FILL);
