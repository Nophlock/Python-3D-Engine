


from components import component
from aabb import AABB
from material import Material
from engine_math import matrix4
from debug_shapes import DebugShapes
from mesh import Mesh



class MeshDebugRenderer(component.Component):

    def __init__(self):
        super().__init__()

        self.identity_matrix = matrix4.Matrix4()
        self.material = Material()
        self.debug_meshes = []


    def get_name(self):
        return "MeshDebugRenderer"

    def render(self, camera, shader):

        shader.send_matrix_4 (shader.get_location("transformation_matrix") , self.identity_matrix)
        shader.send_integer(shader.get_location("has_animation"), 0)

        for i in range(len( self.debug_meshes) ):
            shader.prepare_render(self.debug_meshes[i], self.material)
            self.debug_meshes[i].render()
            shader.unprepare_render(self.debug_meshes[i], self.material)


    def transform_was_modified(self, transform):

        renderer = self.attached_entity.get_component("MeshRenderer")

        if renderer == None:
            return

        for i in range(len(self.debug_meshes)-1, 0, -1):
            del self.debug_meshes[i]

        self.debug_meshes = []
        aabbs = renderer.get_aabbs()

        for i in range(len(aabbs)):
            self.debug_meshes.append(DebugShapes.create_aabb_shape(aabbs[i] ) )
