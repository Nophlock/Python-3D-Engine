
import ctypes
from pyglet.gl 	import *

from vector3 import Vector3
from mesh import Mesh

class CubeMeshLoader:
	
	def get_mesh(self, size):
		vertices = [ 
					-size, -size,  size,
					1.0, 0.0, 0.0,
					 size, -size,  size,
					 1.0, 0.0, 0.0,
					 size,  size,  size,
					 0.0, 1.0, 0.0,
					-size,  size,  size,
					0.0, 1.0, 0.0,
					-size, -size, -size,
					0.0, 0.0, 1.0,
					 size, -size, -size,
					 0.0, 0.0, 1.0,
					 size,  size, -size,
					 1.0, 0.0, 1.0,
					-size,  size, -size,
					1.0, 0.0, 1.0
					]	
					
		ibo = [ 
				0, 1, 2,
				2, 3, 0,
				1, 5, 6,
				6, 2, 1,
				7, 6, 5,
				5, 4, 7,
				4, 0, 3,
				3, 7, 4,
				4, 5, 1,
				1, 0, 4,
				3, 2, 6,
				6, 7, 3
		]
					
		data = {}
		
		data["vbo"] = {}
		data["vbo"]["type"] = GL_ARRAY_BUFFER
		data["vbo"]["size"] = ctypes.sizeof(GLfloat * len(vertices))
		data["vbo"]["data"] = (GLfloat * len(vertices)) (*vertices)
		data["vbo"]["attributes"] = [{}, {}]
		
		data["vbo"]["attributes"][0]["size"] = 3
		data["vbo"]["attributes"][0]["type"] = GL_FLOAT
		data["vbo"]["attributes"][0]["stride"] = 6 * ctypes.sizeof(GLfloat)
		data["vbo"]["attributes"][0]["offset"] = 0
		
		data["vbo"]["attributes"][1]["size"] = 3
		data["vbo"]["attributes"][1]["type"] = GL_FLOAT
		data["vbo"]["attributes"][1]["stride"] = 6 * ctypes.sizeof(GLfloat)
		data["vbo"]["attributes"][1]["offset"] = 3 * ctypes.sizeof(GLfloat)
		
		
		data["ibo"] = {}
		data["ibo"]["type"] = GL_ELEMENT_ARRAY_BUFFER 
		data["ibo"]["size"] = ctypes.sizeof(GLuint * len(ibo))
		data["ibo"]["data"] = (GLuint * len(ibo)) (*ibo)
		
		mesh = Mesh()
		
		mesh.get_buffer().prepare_buffer(GL_TRIANGLES, len(ibo),GL_UNSIGNED_INT, data)
		mesh.get_buffer().create_buffer()
		
		return mesh
	