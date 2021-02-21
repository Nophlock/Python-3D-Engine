

from mesh_buffer_object import MeshBufferObject
from debug_shapes	import DebugShapes

class DebugMesh:

    def __init__(self, scene_mgr, linked_to):
        self.scene_mgr = scene_mgr
        self.linked_to = linked_to
        self.old_shape = None

        self.mesh_buffer_object = MeshBufferObject()


    def update(self, dt):

        aabb = self.linked_to.get_aabb()
        updated = aabb.check_unprojection_min_max_update(self.scene_mgr.transform)

        if aabb != self.old_shape or updated:
            self.old_shape = aabb
            DebugShapes.create_aabb_shape(self, self.old_shape)


    def render(self, scene_manager):
        self.mesh_buffer_object.render()

    def is_animation_root(self):
        return False



    def get_buffer(self):
        return self.mesh_buffer_object

    def has_animations(self):
        return False