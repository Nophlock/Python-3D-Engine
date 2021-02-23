
from pyglet.gl import *

from mesh_buffer_object import MeshBufferObject
from aabb import AABB


class Mesh:

	#TODO: remove the materials from the mesh and make it its own class so we can reuse the mesh with different materials
	def __init__(self, name):
		self.mod_time_stamp = -1
		self.name = name
		self.anim_player = None
		self.aabb = AABB()
		self.informations = None

		self.default_material = None
		self.mesh_buffer_object = MeshBufferObject()


	def set_informations(self, info):
		self.informations = info

	def get_informations(self):
		return self.informations

	def get_name(self):
		return self.name

	def set_aabb(self, aabb):
		self.mod_time_stamp = self.mod_time_stamp + 1
		self.aabb = aabb

	def get_aabb(self):
		return self.aabb


	def get_modified_timestamp(self):
		return self.mod_time_stamp



	def assign_animation_player(self, anim_player):
		self.anim_player = anim_player

	def render(self):
		self.mesh_buffer_object.render()



	def assign_default_material(self, material):
		self.default_material = material


	def get_default_material(self):
		return self.default_material


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
