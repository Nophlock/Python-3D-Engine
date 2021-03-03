
from pyglet.gl  import *
from shader 	import Shader


class NormalShader(Shader):

	def __init__(self, scene_mgr):
		super().__init__()

		self.add_shader( GL_VERTEX_SHADER_ARB	, "data/shaders/normal_shader/normal_vertex.vert"  )
		self.add_shader( GL_FRAGMENT_SHADER_ARB	, "data/shaders/normal_shader/normal_fragment.frag")
		self.compile_shader()

		self.scene_mgr = scene_mgr

		self.locations = {}
		self.locations["time"] = self.get_uniform_location("time")
		self.locations["transformation_matrix"]	= self.get_uniform_location("transformation_matrix")
		self.locations["perspective_matrix"] = self.get_uniform_location("perspective_matrix")
		self.locations["camera_matrix"]	= self.get_uniform_location("camera_matrix")
		self.locations["bone_matrices"]	= self.get_uniform_location("bone_matrices")
		self.locations["has_animation"] = self.get_uniform_location("has_animation")
		self.locations["mesh_color"] = self.get_uniform_location("mesh_color")
		self.locations["has_texture"] = self.get_uniform_location("has_texture")



	def get_location(self, name):

		if  not name in self.locations:
			return "unknown"

		return self.locations[name]

	def prepare_render(self, mesh, material):

		if material == None:
			return

		data = material.get_material_data()
		self.send_vector4(self.get_location("mesh_color"), data["mesh_color"])

		if "diffuse_texture" in data:
			tex_pool = self.scene_mgr.get_texture_pool()
			texture = tex_pool.get_texture(data["diffuse_texture"])

			self.send_integer(self.get_location("has_texture"), 1)

			if texture != None:
				glEnable(texture["texture"].target)
				glBindTexture(texture["texture"].target, texture["texture"].id)
		else:
			self.send_integer(self.get_location("has_texture"), 0)







	def unprepare_render(self, mesh, material):

		if material == None:
			return

		data = material.get_material_data()

		if "diffuse_texture" in data:
			tex_pool = self.scene_mgr.get_texture_pool()
			texture = tex_pool.get_texture(data["diffuse_texture"])

			if texture != None:
				glDisable(texture["texture"].target)
				glBindTexture(texture["texture"].target, 0)
