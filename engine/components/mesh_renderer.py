
from components import component
from aabb import AABB
from material import Material

class MeshRenderer(component.Component):

    def __init__(self, meshes):
        super().__init__()

        _aabb = meshes[0].get_aabb()

        self.anim_player = None
        self.meshes = meshes
        self.materials = []
        self.aabb = AABB(_aabb.min, _aabb.max, True) #for now this will do the trick

        for i in range(len(self.meshes)):
            self.materials.append( self.meshes[i].get_default_material().get_copy() )

        if meshes[0].has_animations():
            self.anim_player = meshes[0].get_new_animation_player()




    def get_name(self):
        return "MeshRenderer"

    def get_meshes(self):
        return self.meshes

    def get_aabbs(self):
        return [self.aabb]

    def get_materials(self):
        return self.materials


    def play_animation(self, anim_name, anim_speed):

        if self.anim_player == None:
            return

        self.anim_player.play_animation("idle", anim_speed)


    def update(self, dt):

        if self.anim_player != None:
            self.anim_player.update(dt)

            _aabb = self.anim_player.get_current_aabb()
            self.aabb.set_min_max(_aabb.min, _aabb.max)
            self.attached_entity.transform_was_modified()





    def render(self, camera, shader):

        if self.anim_player == None:
            shader.send_integer(shader.get_location("has_animation"), 0)
        else:
            shader.send_integer(shader.get_location("has_animation"), 1)
            shader.send_matrix3x4_array( shader.get_location("bone_matrices"), self.anim_player.get_animation_matrices())


        shader.send_matrix_4 (shader.get_location("transformation_matrix") , self.attached_entity.get_transform().get_transformation_matrix())

        for i in range(len( self.meshes) ):
            shader.prepare_render(self.meshes[i], self.materials[i])
            self.meshes[i].render()
            shader.unprepare_render(self.meshes[i], self.materials[i])


    def get_aabb(self):
        return self.aabb



    def transform_was_modified(self, transform):
        self.aabb.calculate_aabb_unprojected(transform)
