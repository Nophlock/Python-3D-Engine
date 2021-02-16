
from pyglet.gl  import *
from shader 	import Shader


class NormalShader(Shader):

	def __init__(self):
		super().__init__()

		self.addShader( GL_VERTEX_SHADER_ARB	, "data/shaders/normal_vertex.vert"  )
		self.addShader( GL_FRAGMENT_SHADER_ARB	, "data/shaders/normal_fragment.frag")
		self.compileShader()

		self.locations 							= {}
		self.locations["time"]					= self.getUniformLocation("time")
		self.locations["transformation_matrix"]	= self.getUniformLocation("transformation_matrix")
		self.locations["perspective_matrix"]	= self.getUniformLocation("perspective_matrix")
		self.locations["camera_matrix"]			= self.getUniformLocation("camera_matrix")
		self.locations["bone_matrices"]			= self.getUniformLocation("bone_matrices")



	def get_location(self, name):

		if  not name in self.locations:
			return "unknown"

		return self.locations[name]

	#fixme, sending the matrices here is probably not a good way
	def prepare_render(self, mesh):

		if mesh.is_animation_root():
			self.send_matrix3x4_array( self.get_location("bone_matrices"), mesh.get_animation_player().get_animation_matrices())
