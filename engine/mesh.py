
from pyglet.gl import *

from mesh_buffer_object import MeshBufferObject
from iqm_mesh_animation_player import IQMMeshAnimationPlayer
from aabb import AABB


class Mesh:

	#TODO: remove the name stuff and use a id system or something like that
	def __init__(self, name):
		self.name = name
		self.aabb = AABB()
		self.mesh_data = None
		self.informations = None
		self.animation_class = None

		self.default_material = None
		self.mesh_buffer_object = MeshBufferObject()


	def set_informations(self, info):
		self.informations = info

	def get_informations(self):
		return self.informations

	def get_name(self):
		return self.name

	def set_aabb(self, aabb):
		self.aabb = aabb

	def get_aabb(self):
		return self.aabb


	def get_modified_timestamp(self):
		return self.mod_time_stamp


	def render(self):
		self.mesh_buffer_object.render()


	def assign_default_material(self, material):
		self.default_material = material


	def get_default_material(self):
		return self.default_material


	def get_buffer(self):
		return self.mesh_buffer_object

	def has_animations(self):
		return self.animation_class != None

	def set_animation_player_class(self, anim_player):
		self.animation_class = anim_player

	def get_animation_player_class(self):
		return self.animation_class

	def get_new_animation_player(self):
		return self.animation_class(self.mesh_data)

	def assign_mesh_data(self, mesh_data):
		self.mesh_data = mesh_data


	def get_animation_player(self):
		return self.anim_player
