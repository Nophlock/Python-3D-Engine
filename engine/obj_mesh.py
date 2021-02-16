import ctypes
import math

from pyglet.gl 	import *

from vector3 import Vector3
from mesh import Mesh

FACE_MAPPING = {}
FACE_MAPPING[3] = [GL_TRIANGLES, 3]
FACE_MAPPING[4] = [GL_QUADS, 4]

class ObjMeshLoader:
	
	def get_mesh(self, file_path):
		data = self.read_file(file_path)
		return self.generate_mesh(data)
		
		
	def read_file(self, file_path):

		data = {}
		data["type"] = GL_TRIANGLES
		
		data["raw_vertices"] = []
		data["raw_tex_coords"] = []
		data["raw_normals"] = []
		
		data["aabb"] = {}
		data["aabb"]["min"] = Vector3(math.inf, math.inf, math.inf)
		data["aabb"]["max"] = Vector3(-math.inf,-math.inf,-math.inf)
		
		data["vertices"] = []
		data["indices"] = []
	
		for line in open(file_path, "r"):
			
			if line.startswith("#"):
				continue
				
			values = line.split()
			
			if not values:
				continue
				
			if values[0] == "v":
				x = float(values[1])
				y = float(values[2])
				z = float(values[3])
			
				data["raw_vertices"].append(x)
				data["raw_vertices"].append(y)
				data["raw_vertices"].append(z)
				
				data["aabb"]["min"].x = min(data["aabb"]["min"].x, x) 
				data["aabb"]["min"].y = min(data["aabb"]["min"].y, y)
				data["aabb"]["min"].z = min(data["aabb"]["min"].z, z)
				
				data["aabb"]["max"].x = max(data["aabb"]["max"].x, x) 
				data["aabb"]["max"].y = max(data["aabb"]["max"].y, y)
				data["aabb"]["max"].z = max(data["aabb"]["max"].z, z)
				
			if values[0] == "vt":
				data["raw_tex_coords"].append(float(values[1]) )
				data["raw_tex_coords"].append(float(values[2]) )
				
			if values[0] == "vn":
				data["raw_normals"].append(float(values[1]) )
				data["raw_normals"].append(float(values[2]) )
				data["raw_normals"].append(float(values[3]) )
				
			if values[0] == "f":
			
				data["type"] = FACE_MAPPING[len(values)-1]
				
				for v in values[1:]:
					vals = v.split("/")
					
					v_indx = (int(vals[0])-1) * 3
					tx_indx = (int(vals[1])-1) * 2
					n_indx = (int(vals[2])-1) * 3
					
					data["vertices"].append(data["raw_vertices"][v_indx] )
					data["vertices"].append(data["raw_vertices"][v_indx+1] )
					data["vertices"].append(data["raw_vertices"][v_indx+2] )
					
					data["vertices"].append(data["raw_normals"][n_indx] )
					data["vertices"].append(data["raw_normals"][n_indx+1] )
					data["vertices"].append(data["raw_normals"][n_indx+2] )
					
					data["vertices"].append(data["raw_tex_coords"][tx_indx] )
					data["vertices"].append(data["raw_tex_coords"][tx_indx+1] )
					
					data["indices"].append( len(data["indices"]) )
					
					
		return data

					
	def generate_mesh(self, data):
		mesh_data = {}
		
		mesh_data["vbo"] = {}
		mesh_data["vbo"]["type"] = GL_ARRAY_BUFFER
		mesh_data["vbo"]["size"] = ctypes.sizeof(GLfloat * len(data["vertices"]))
		mesh_data["vbo"]["data"] = (GLfloat * len(data["vertices"])) (*data["vertices"])
		mesh_data["vbo"]["attributes"] = []
		
		mesh_data["vbo"]["attributes"].append({})
		mesh_data["vbo"]["attributes"][0]["size"] = 3
		mesh_data["vbo"]["attributes"][0]["type"] = GL_FLOAT
		mesh_data["vbo"]["attributes"][0]["stride"] = 8 * ctypes.sizeof(GLfloat)#every 6 byte defines the next start_position of an vertex
		mesh_data["vbo"]["attributes"][0]["offset"] = 0
		
		mesh_data["vbo"]["attributes"].append({})
		mesh_data["vbo"]["attributes"][1]["size"] = 3
		mesh_data["vbo"]["attributes"][1]["type"] = GL_FLOAT
		mesh_data["vbo"]["attributes"][1]["stride"] = 8 * ctypes.sizeof(GLfloat)#start_pos
		mesh_data["vbo"]["attributes"][1]["offset"] = 3 * ctypes.sizeof(GLfloat)#start_pos + offset
		
		mesh_data["vbo"]["attributes"].append({})
		mesh_data["vbo"]["attributes"][2]["size"] = 2
		mesh_data["vbo"]["attributes"][2]["type"] = GL_FLOAT
		mesh_data["vbo"]["attributes"][2]["stride"] = 8 * ctypes.sizeof(GLfloat)#start_pos
		mesh_data["vbo"]["attributes"][2]["offset"] = 6 * ctypes.sizeof(GLfloat)#start_pos + offset
		
		mesh_data["ibo"] = {}
		mesh_data["ibo"]["type"] = GL_ELEMENT_ARRAY_BUFFER 
		mesh_data["ibo"]["size"] = ctypes.sizeof(GLuint * len(data["indices"]) )
		mesh_data["ibo"]["data"] = (GLuint * len(data["indices"])) (*data["indices"])
		
		mesh = Mesh()
		mesh.get_buffer().prepare_buffer(data["type"][0], len(data["indices"]),GL_UNSIGNED_INT, mesh_data)
		mesh.get_buffer().create_buffer()

		return mesh