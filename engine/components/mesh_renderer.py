
from components import component
from aabb import AABB
from material import Material

class MeshRenderer(component.Component):

    def __init__(self, meshes):
        super().__init__()

        _aabb = meshes[0].get_aabb()

        self.meshes = meshes
        self.materials = []
        self.aabb = AABB(_aabb.min, _aabb.max, True) #for now this will do the trick

        for i in range(len(self.meshes)):
            self.materials.append( self.meshes[i].get_default_material().get_copy() )




    def get_name(self):
        return "MeshRenderer"

    def get_meshes(self):
        return self.meshes

    def get_aabbs(self):
        return [self.aabb]

    def get_materials(self):
        return self.materials

    #todo: make the animation player work again
    def update(self, dt):
        pass

#        for i in range(len(self.meshes)):
#
#            if self.meshes[i].is_animation_root() and self.meshes[i].is_animation_root():
#                self.meshes[i].get_animation_player().update(dt)



    def render(self, camera, shader):

        shader.send_matrix_4 (shader.get_location("transformation_matrix") , self.attached_entity.get_transform().get_transformation_matrix())

        for i in range(len( self.meshes) ):
            shader.prepare_render(self.meshes[i], self.materials[i])
            self.meshes[i].render()
            shader.unprepare_render(self.meshes[i], self.materials[i])


    def get_aabb(self):
        return self.aabb



    def transform_was_modified(self, transform):
        self.aabb.calculate_aabb_unprojected(transform)
