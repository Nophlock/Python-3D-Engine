
from pyglet.gl  import *
from shader 	import Shader


class NormalShader(Shader):

	def __init__(self):
		super().__init__()

		self.add_shader( GL_VERTEX_SHADER_ARB	, "data/shaders/normal_shader/normal_vertex.vert"  )
		self.add_shader( GL_FRAGMENT_SHADER_ARB	, "data/shaders/normal_shader/normal_fragment.frag")
		self.compile_shader()

		self.locations = {}
		self.locations["time"] = self.get_uniform_location("time")
		self.locations["transformation_matrix"]	= self.get_uniform_location("transformation_matrix")
		self.locations["perspective_matrix"] = self.get_uniform_location("perspective_matrix")
		self.locations["camera_matrix"]	= self.get_uniform_location("camera_matrix")
		self.locations["bone_matrices"]	= self.get_uniform_location("bone_matrices")
		self.locations["has_animation"] = self.get_uniform_location("has_animation")



	def get_location(self, name):

		if  not name in self.locations:
			return "unknown"

		return self.locations[name]

	def prepare_render(self, mesh):

		if mesh.has_animations():
			self.send_integer( self.get_location("has_animation"), 1)
		else:
			self.send_integer( self.get_location("has_animation"), 0)

		if mesh.is_animation_root():
			self.send_matrix3x4_array( self.get_location("bone_matrices"), mesh.get_animation_player().get_animation_matrices())
