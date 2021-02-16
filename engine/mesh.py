
from mesh_buffer_object import MeshBufferObject
from pyglet.gl import *

class Mesh:

	def __init__(self, name):
		self.name = name
		self.materials = {}
		self.anim_player = None

		self.mesh_buffer_object = MeshBufferObject()


	def get_name():
		return self.name


	def assign_animation_player(self, anim_player):
		self.anim_player = anim_player

	def render(self, scene_manager):

		material = self.get_material("diffuse")
		texture = None

		if material != None:
			tex_pool = scene_manager.get_texture_pool()
			texture = tex_pool.get_texture(material)


			if texture != None:
				glEnable(texture["texture"].target)
				glBindTexture(texture["texture"].target, texture["texture"].id)

		self.mesh_buffer_object.render()

		if material != None:
			if texture != None:
				glDisable(texture["texture"].target)
				glBindTexture(texture["texture"].target, 0)


	def assign_material(self, material_type, material_name):
		self.materials[material_type] = material_name


	def get_material(self, material_type):

		if material_type in self.materials:
			return self.materials[material_type]

		return None


	def get_buffer(self):
		return self.mesh_buffer_object

	def has_animations(self):
		return self.anim_player != None

	def is_animation_root(self):
		if self.has_animations() and self.anim_player.is_root(self):
			return True

		return False

	def get_animation_player(self):
		return self.anim_player
