import ctypes
import math
import os

from pyglet.gl 	import *

from vector3 import Vector3
from aabb import AABB
from mesh import Mesh

FACE_MAPPING = {}
FACE_MAPPING[3] = [GL_TRIANGLES, 3]
FACE_MAPPING[4] = [GL_QUADS, 4]

class OBJMeshLoader:

	def __init__(self, scene_manager):
		self.scene_manager = scene_manager

	def get_mesh(self, file_path):
		data = self.read_file(file_path)
		return self.generate_mesh(data)


	def read_file(self, file_path):

		tex_pool = self.scene_manager.get_texture_pool()

		meshes = []
		mesh_data = {}
		global_data = {}
		line_count = 0
		calc_face_offset = 0

		global_data["raw_vertices"] = []
		global_data["raw_tex_coords"] = []
		global_data["raw_normals"] = []


		for line in open(file_path, "r"):

			if line.startswith("#"):
				continue

			values = line.split()

			if not values:
				continue

			if values[0] == "o":

				if "name" in mesh_data:
					meshes.append(mesh_data)

				mesh_data = {}

				mesh_data["name"] = values[1]
				mesh_data["type"] = GL_TRIANGLES

				mesh_data["vertices"] = []
				mesh_data["indices"] = []
				mesh_data["diffuse_texture"] = ""
				mesh_data["aabb"] = AABB(Vector3(math.inf, math.inf, math.inf), Vector3(-math.inf, -math.inf, -math.inf))


			if values[0] == "v":
				x = float(values[1])
				y = float(values[2])
				z = float(values[3])

				global_data["raw_vertices"].append(x)
				global_data["raw_vertices"].append(y)
				global_data["raw_vertices"].append(z)

				mesh_data["aabb"].min.x = min(mesh_data["aabb"].min.x, x)
				mesh_data["aabb"].min.y = min(mesh_data["aabb"].min.y, y)
				mesh_data["aabb"].min.z = min(mesh_data["aabb"].min.z, z)

				mesh_data["aabb"].max.x = max(mesh_data["aabb"].max.x, x)
				mesh_data["aabb"].max.y = max(mesh_data["aabb"].max.y, y)
				mesh_data["aabb"].max.z = max(mesh_data["aabb"].max.z, z)

			if values[0] == "vt":
				global_data["raw_tex_coords"].append(float(values[1]) )
				global_data["raw_tex_coords"].append(float(values[2]) )

			if values[0] == "vn":
				global_data["raw_normals"].append(float(values[1]) )
				global_data["raw_normals"].append(float(values[2]) )
				global_data["raw_normals"].append(float(values[3]) )

			if values[0] == "f":

				mesh_data["type"] = FACE_MAPPING[len(values)-1]

				for v in values[1:]:
					vals = v.split("/")

					v_indx = (int(vals[0]) - 1) * 3
					tx_indx = (int(vals[1]) - 1) * 2
					n_indx = (int(vals[2]) - 1) * 3

					mesh_data["vertices"].append(global_data["raw_vertices"][v_indx] )
					mesh_data["vertices"].append(global_data["raw_vertices"][v_indx+1] )
					mesh_data["vertices"].append(global_data["raw_vertices"][v_indx+2] )

					mesh_data["vertices"].append(global_data["raw_tex_coords"][tx_indx] )
					mesh_data["vertices"].append(global_data["raw_tex_coords"][tx_indx+1] )

					mesh_data["vertices"].append(global_data["raw_normals"][n_indx] )
					mesh_data["vertices"].append(global_data["raw_normals"][n_indx+1] )
					mesh_data["vertices"].append(global_data["raw_normals"][n_indx+2] )

					mesh_data["indices"].append( len(mesh_data["indices"]) )

			line_count = line_count + 1

		meshes.append(mesh_data)

		base_path = os.path.dirname(file_path)
		base_name = os.path.basename(os.path.splitext(file_path)[0])

		if os.path.isfile(base_path + "/" + base_name + ".mtl"):

			for line in open(base_path + "/" + base_name + ".mtl", "r"):

				if line.startswith("#"):
					continue

				values = line.split()

				if not values:
					continue

				if values[0] == "map_Kd":
					tex_pool.load_texture(values[1], base_path, base_path + "/" + values[1])#load the material texture

					for i in range(len(meshes)):
						meshes[i]["diffuse_texture"] = values[1]


		return meshes


	def generate_mesh(self, data):

		meshes = []

		for i in range(len(data)):

			c_data = data[i]
			mesh_data = {}

			mesh_data["vbo"] = {}
			mesh_data["vbo"]["type"] = GL_ARRAY_BUFFER
			mesh_data["vbo"]["size"] = ctypes.sizeof(GLfloat * len(c_data["vertices"]))
			mesh_data["vbo"]["data"] = (GLfloat * len(c_data["vertices"])) (*c_data["vertices"])
			mesh_data["vbo"]["attributes"] = []

			mesh_data["vbo"]["attributes"].append({})
			mesh_data["vbo"]["attributes"][0]["size"] = 3
			mesh_data["vbo"]["attributes"][0]["type"] = GL_FLOAT
			mesh_data["vbo"]["attributes"][0]["stride"] = 8 * ctypes.sizeof(GLfloat)#every 6 byte defines the next start_position of an vertex
			mesh_data["vbo"]["attributes"][0]["offset"] = 0
			mesh_data["vbo"]["attributes"][0]["normalized"] = GL_FALSE

			mesh_data["vbo"]["attributes"].append({})
			mesh_data["vbo"]["attributes"][1]["size"] = 3
			mesh_data["vbo"]["attributes"][1]["type"] = GL_FLOAT
			mesh_data["vbo"]["attributes"][1]["stride"] = 8 * ctypes.sizeof(GLfloat)#start_pos
			mesh_data["vbo"]["attributes"][1]["offset"] = 3 * ctypes.sizeof(GLfloat)#start_pos + offset
			mesh_data["vbo"]["attributes"][1]["normalized"] = GL_FALSE

			mesh_data["vbo"]["attributes"].append({})
			mesh_data["vbo"]["attributes"][2]["size"] = 2
			mesh_data["vbo"]["attributes"][2]["type"] = GL_FLOAT
			mesh_data["vbo"]["attributes"][2]["stride"] = 8 * ctypes.sizeof(GLfloat)#start_pos
			mesh_data["vbo"]["attributes"][2]["offset"] = 6 * ctypes.sizeof(GLfloat)#start_pos + offset
			mesh_data["vbo"]["attributes"][2]["normalized"] = GL_FALSE


			mesh_data["ibo"] = {}
			mesh_data["ibo"]["type"] = GL_ELEMENT_ARRAY_BUFFER
			mesh_data["ibo"]["size"] = ctypes.sizeof(GLuint * len(c_data["indices"]) )
			mesh_data["ibo"]["data"] = (GLuint * len(c_data["indices"])) (*c_data["indices"])

			c_data["aabb"].calculate_knots()

			mesh = Mesh(c_data["name"])
			mesh.get_buffer().prepare_buffer(c_data["type"][0], len(c_data["indices"]),GL_UNSIGNED_INT, mesh_data)
			mesh.get_buffer().create_buffer()
			mesh.set_aabb(c_data["aabb"])

			if c_data["diffuse_texture"] != "":
				mesh.assign_material("diffuse", c_data["diffuse_texture"])

			meshes.append(mesh)


		return meshes
