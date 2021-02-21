import ctypes
import math
import struct
import os

from pyglet.gl import *

from engine_math import vector3
from engine_math import quaternion

from mesh import Mesh
from iqm_mesh_animation_player import IQMMeshAnimationPlayer
from aabb import AABB

VERTEX_ORDER = [
	"vertices",
	"texcoord",
	"normal",
	"tangent",
	"blend_index",
	"blend_weight",
	"color",
	"reserved_1",
	"reserved_2",
	"reserved_3",
	"custom"
]


VERTEX_FORMAT = [
	[GL_BYTE, GLbyte],
	[GL_UNSIGNED_BYTE, GLubyte],
	[GL_SHORT, GLshort],
	[GL_UNSIGNED_SHORT, GLushort],
	[GL_INT, GLint],
	[GL_UNSIGNED_INT, GLuint],
	[GL_FLOAT, GLfloat], #note that this is meant to be half or half float, but pyglet doesnt have this, maybe theres an workaround but normaly no one use half precision anyway
	[GL_FLOAT, GLfloat],
	[GL_DOUBLE, GLdouble]
]

IQM_TRIANGLE_SIZE = 3

class IQMLoader:

	def __init__(self, scene_manager):
		self.scene_manager = scene_manager

	def get_meshs(self, file_path):
		mesh_data = self.load_file(file_path)
		meshes = self.generate_mesh(mesh_data)

		if mesh_data["animation_data"] != None:
			anim_player = IQMMeshAnimationPlayer(meshes, mesh_data)

			for i in range(len(meshes)):
				meshes[i].assign_animation_player(anim_player)

		return meshes


	def load_file(self, file_path):

		mesh_data = {}
		abs_file_path = os.path.abspath(file_path)

		with open(abs_file_path, "rb") as file:
			magic = file.read(16)

			if magic.decode("utf-8") != "INTERQUAKEMODEL\0":
				mesh_data["error"] = "Doesnt match magic"
				return mesh_data

			header = {}
			#reads the header informations
			header["version"] = int.from_bytes(file.read(4), "little")
			header["filesize"] = int.from_bytes(file.read(4), "little")
			header["flags"] = int.from_bytes(file.read(4), "little")
			header["num_text"] = int.from_bytes(file.read(4), "little")
			header["ofs_text"] = int.from_bytes(file.read(4), "little")
			header["num_meshes"] = int.from_bytes(file.read(4), "little")
			header["ofs_meshes"] = int.from_bytes(file.read(4), "little")
			header["num_vertexarr"] = int.from_bytes(file.read(4), "little")
			header["num_vertexes"] = int.from_bytes(file.read(4), "little")
			header["ofs_vertexarr"] = int.from_bytes(file.read(4), "little")
			header["num_triangle"] = int.from_bytes(file.read(4), "little")
			header["ofs_triangle"] = int.from_bytes(file.read(4), "little")
			header["ofs_adjacency"] = int.from_bytes(file.read(4), "little")
			header["num_joints"] = int.from_bytes(file.read(4), "little")
			header["ofs_joints"] = int.from_bytes(file.read(4), "little")
			header["num_poses"] = int.from_bytes(file.read(4), "little")
			header["ofs_poses"] = int.from_bytes(file.read(4), "little")
			header["num_anims"] = int.from_bytes(file.read(4), "little")
			header["ofs_anims"] = int.from_bytes(file.read(4), "little")
			header["num_frames"] = int.from_bytes(file.read(4), "little")
			header["num_framechannels"] = int.from_bytes(file.read(4), "little")
			header["ofs_frames"] = int.from_bytes(file.read(4), "little")
			header["ofs_bounds"] = int.from_bytes(file.read(4), "little")
			header["num_comment"] = int.from_bytes(file.read(4), "little")
			header["ofs_comment"] = int.from_bytes(file.read(4), "little")
			header["num_extension"] = int.from_bytes(file.read(4), "little")
			header["ofs_extension"] = int.from_bytes(file.read(4), "little")


			if header["version"] != 2:
				mesh_data["error"] = "Model is outdated, only Version 2 is supported"
				return mesh_data



			indices = []
			vertex_arrays = []
			meshes = []

			#read the text parts
			file.seek(header["ofs_text"])
			text_blob = file.read(header["num_text"]).decode("utf-8")

			#reads the mesh vertex informations
			file.seek(header["ofs_vertexarr"])

			for i in range(header["num_vertexarr"]):
				vertex_data = {}

				vertex_data["type"] = int.from_bytes(file.read(4), "little")
				vertex_data["flags"] = int.from_bytes(file.read(4), "little")
				vertex_data["format"] = int.from_bytes(file.read(4), "little")
				vertex_data["size"] = int.from_bytes(file.read(4), "little")
				vertex_data["offset"] = int.from_bytes(file.read(4), "little")
				vertex_data["num_entries"] = header["num_vertexes"] * vertex_data["size"]
				vertex_data["str_type"] = VERTEX_ORDER[i]

				vertex_arrays.append(vertex_data)




			for i in range(len(vertex_arrays)):
				data = []

				file.seek(vertex_arrays[i]["offset"])

				for _ in range(vertex_arrays[i]["num_entries"]):

					gl_type = VERTEX_FORMAT[ vertex_arrays[i]["format"] ][0]
					value = 0

					if gl_type == GL_FLOAT:
						(value,) = struct.unpack("f", file.read(4))
					elif gl_type == GL_BYTE:
						value = int.from_bytes(file.read(1), byteorder = "little", signed = True)
					elif gl_type == GL_UNSIGNED_BYTE:
						value = int.from_bytes(file.read(1), "little")
					elif gl_type == GL_INT:
						value = int.from_bytes(file.read(4), "little", signed= True)
					elif gl_type == GL_UINT:
						value = int.from_bytes(file.read(4), "little")
					else:
						print("IQM-Loader: Not implemented datatype - ", gl_type)


					data.append( value )

				vertex_arrays[i]["data"] = data

			#reads the ibo-data
			file.seek(header["ofs_triangle"])

			for i in range(header["num_triangle"]):
				indices.append( int.from_bytes(file.read(4), "little") )
				indices.append( int.from_bytes(file.read(4), "little") )
				indices.append( int.from_bytes(file.read(4), "little") )


			#reads the mesh information to later load them
			file.seek(header["ofs_meshes"])
			base_path = os.path.dirname(file_path)
			tex_pool = self.scene_manager.get_texture_pool()


			for i in range(header["num_meshes"]):
				mesh_informations = {}

				mesh_informations["name"] = int.from_bytes(file.read(4), "little")
				mesh_informations["material"] = int.from_bytes(file.read(4), "little")
				mesh_informations["first_vertex"] = int.from_bytes(file.read(4), "little")
				mesh_informations["num_vertices"] = int.from_bytes(file.read(4), "little")
				mesh_informations["first_triangle"] = int.from_bytes(file.read(4), "little")
				mesh_informations["num_triangle"] = int.from_bytes(file.read(4), "little")
				mesh_informations["str_name"] = self.resolve_name(text_blob, mesh_informations["name"])
				mesh_informations["str_material"] = self.resolve_name(text_blob, mesh_informations["material"])

				meshes.append(mesh_informations)
				tex_pool.load_texture(mesh_informations["str_material"], base_path, mesh_informations["str_material"])#load the material texture


			mesh_data["animation_data"] = self.load_animation(header, file, text_blob)


			#reads the stored bbox (should be atleast one)
			mesh_data["bboxes"] = []

			file.seek(header["ofs_bounds"])

			for i in range(header["num_frames"]):
				(min_x,) = struct.unpack("f", file.read(4))
				(min_y,) = struct.unpack("f", file.read(4))
				(min_z,) = struct.unpack("f", file.read(4))

				(max_x,) = struct.unpack("f", file.read(4))
				(max_y,) = struct.unpack("f", file.read(4))
				(max_z,) = struct.unpack("f", file.read(4))

				(xyradius,) = struct.unpack("f", file.read(4))
				(radius,) = struct.unpack("f", file.read(4))

				aabb = AABB(vector3.Vector3(min_x,min_y,min_z), vector3.Vector3(max_x,max_y,max_z), True)

				mesh_data["bboxes"].append(aabb)


		mesh_data["buffers"] = []
		mesh_data["indices"] = indices
		mesh_data["mesh_informations"] = meshes

		for i in range(len(vertex_arrays) ):
			buffer = {}
			buffer["size"] = vertex_arrays[i]["size"]
			buffer["data"] = vertex_arrays[i]["data"]
			buffer["data_type"] = VERTEX_FORMAT[ vertex_arrays[i]["format"] ]

			buffer["normalized"] = GL_FALSE

			if i == 5:
				buffer["normalized"] = GL_TRUE

			mesh_data["buffers"].append(buffer)

		return mesh_data

	#load all animation data, note that frames are keeps track of any pose for any animation for any time ()
	def load_animation(self, header, file, text_blob):


		if header["num_anims"] == 0:
			return None

		animation_data = {}
		animation_data["frame_positions"] = []

		joints = []
		poses = []
		animations = []
		frames = []

		#load all joints if we have any
		if header["ofs_joints"] != 0:
			file.seek(header["ofs_joints"])

			for i in range(header["num_joints"]):
				joint = {}

				joint["name"] = self.resolve_name(text_blob, int.from_bytes(file.read(4), "little"))
				joint["parent"] = int.from_bytes(file.read(4), byteorder = "little", signed = True)

				(tx,) = struct.unpack("f", file.read(4))
				(ty,) = struct.unpack("f", file.read(4))
				(tz,) = struct.unpack("f", file.read(4))

				(rx,) = struct.unpack("f", file.read(4))
				(ry,) = struct.unpack("f", file.read(4))
				(rz,) = struct.unpack("f", file.read(4))
				(rw,) = struct.unpack("f", file.read(4))

				(sx,) = struct.unpack("f", file.read(4))
				(sy,) = struct.unpack("f", file.read(4))
				(sz,) = struct.unpack("f", file.read(4))

				joint["translate"] = vector3.Vector3(tx,ty,tz)
				joint["rotate"] = quaternion.Quaternion(vector3.Vector3(rx,ry,rz),rw).get_normalized()
				joint["scale"] = vector3.Vector3(sx,sy,sz)

				joints.append(joint)

			animation_data["joints"] = joints


		#load all animations if we have any
		if header["ofs_anims"] != 0:
			file.seek(header["ofs_anims"])

			for i in range(header["num_anims"]):
				animation = {}

				animation["name"] = self.resolve_name(text_blob, int.from_bytes(file.read(4), "little"))
				animation["first_frame"] = int.from_bytes(file.read(4), "little")
				animation["num_frames"] = int.from_bytes(file.read(4), "little")

				(framerate,) = struct.unpack("f", file.read(4))

				animation["framerate"] = framerate
				animation["flags"] = int.from_bytes(file.read(4), "little")

				animations.append(animation)



			animation_data["animations"] = animations

		#load all frame_data and translate them if we have any
		if header["ofs_poses"] != 0:
			file.seek(header["ofs_frames"])

			for i in range(header["num_frames"] * header["num_framechannels"]):
				value = int.from_bytes(file.read(2), "little")

				frames.append(value)

			file.seek(header["ofs_poses"])

			#load all poses, but in raw, since we need to modify/stretch them to match them witch all animation we will have
			for i in range(header["num_poses"]):
				pose = {}

				pose["parent"] = int.from_bytes(file.read(4), byteorder = "little", signed = True)
				pose["channel_mask"] = int.from_bytes(file.read(4), "little")

				channel_offset = []
				channel_scale = []

				for i in range(10):
					(val,) = struct.unpack("f", file.read(4))
					channel_offset.append(val)

				for i in range(10):
					(val,) = struct.unpack("f", file.read(4))
					channel_scale.append(val)


				pose["channel_offset"] = channel_offset #translation, rotation, scale
				pose["channel_scale"] = channel_scale
				poses.append(pose)

			animation_data["poses"] = poses
			frame_index = 0

			#remap all our animation data
			for i in range(header["num_frames"]):
				animation_data["frame_positions"].append([])

				for j in range(header["num_poses"]):

					channel_mask = poses[j]["channel_mask"]
					channel_offset = poses[j]["channel_offset"]
					channel_scale = poses[j]["channel_scale"]

					translate = vector3.Vector3()
					scale = vector3.Vector3()


					translate.x, frame_index = self.extract_frame_data( channel_offset, channel_mask, channel_scale, frames, frame_index, 0)
					translate.y, frame_index = self.extract_frame_data( channel_offset, channel_mask, channel_scale, frames, frame_index, 1)
					translate.z, frame_index = self.extract_frame_data( channel_offset, channel_mask, channel_scale, frames, frame_index, 2)

					rx, frame_index = self.extract_frame_data( channel_offset, channel_mask, channel_scale, frames, frame_index, 3)
					ry, frame_index = self.extract_frame_data( channel_offset, channel_mask, channel_scale, frames, frame_index, 4)
					rz, frame_index = self.extract_frame_data( channel_offset, channel_mask, channel_scale, frames, frame_index, 5)
					rw, frame_index = self.extract_frame_data( channel_offset, channel_mask, channel_scale, frames, frame_index, 6)

					scale.x, frame_index = self.extract_frame_data( channel_offset, channel_mask, channel_scale, frames, frame_index, 7)
					scale.y, frame_index = self.extract_frame_data( channel_offset, channel_mask, channel_scale, frames, frame_index, 8)
					scale.z, frame_index = self.extract_frame_data( channel_offset, channel_mask, channel_scale, frames, frame_index, 9)

					rotation = quaternion.Quaternion(vector3.Vector3(rx,ry,rz), rw)#we need to assign it here with the constructor, otherwise everything explodes for some reason ...

					animation_data["frame_positions"][i].append({"pose": poses[j], "translate": translate, "rotate": rotation, "scale": scale})

		return animation_data

	def extract_frame_data(self, channel_offset, channel_mask, channel_scale, frame_data, frame_index, index):

		value = channel_offset[index]

		if (channel_mask & (1 << index)) > 0:
			return (value + frame_data[frame_index] * channel_scale[index]), frame_index + 1

		return value, frame_index


	def resolve_name(self, text_blob, position):
		copy_str = ""
		c_pos = position


		while True:

			if c_pos >= len(text_blob):
				break
			elif text_blob[c_pos] == " " or text_blob[c_pos] == "" or text_blob[c_pos] == "\x00":
				break

			copy_str = copy_str + text_blob[c_pos]
			c_pos = c_pos + 1

		return copy_str

	def generate_mesh(self, data):

		if "error" in data:
			print(data["error"])
			return Mesh()


		meshes = []

		for i in range( len(data["mesh_informations"]) ):

			mesh_data = {}
			mesh_infos = {}

			indi_clip = ( data["mesh_informations"][i]["first_triangle"] * IQM_TRIANGLE_SIZE, (data["mesh_informations"][i]["first_triangle"] + data["mesh_informations"][i]["num_triangle"]) * IQM_TRIANGLE_SIZE )
			used_indices = data["indices"][ indi_clip[0]:indi_clip[1] ]

			mesh_infos["num_triangles"] = data["mesh_informations"][i]["num_triangle"]
			mesh_infos["num_vertices"] = data["mesh_informations"][i]["num_vertices"]
			mesh_infos["num_bones"] = 0

			if "animation_data" in data:
				mesh_infos["num_bones"] = len( data["animation_data"]["joints"] )

			for j in range(len(data["buffers"]) ):

				name = "str_" + str(j)
				buf = data["buffers"][j]

				type = buf["data_type"][1]
				buf_data = buf["data"]
				mesh_data[name] = {}


				mesh_data[name]["type"] = GL_ARRAY_BUFFER
				mesh_data[name]["size"] = ctypes.sizeof(type * len(buf_data))

				mesh_data[name]["data"] = (type * len(buf_data)) (*buf_data)
				mesh_data[name]["attributes"] = [{}]

				mesh_data[name]["attributes"][0]["size"] = buf["size"]
				mesh_data[name]["attributes"][0]["normalized"] = buf["normalized"]
				mesh_data[name]["attributes"][0]["type"] = buf["data_type"][0]
				mesh_data[name]["attributes"][0]["stride"] = 0
				mesh_data[name]["attributes"][0]["offset"] = 0

			mesh_data["ibo"] = {}
			mesh_data["ibo"]["type"] = GL_ELEMENT_ARRAY_BUFFER
			mesh_data["ibo"]["size"] = ctypes.sizeof(GLuint * len(used_indices) )
			mesh_data["ibo"]["data"] = (GLuint * len(used_indices)) (*used_indices)

			mesh = Mesh(data["mesh_informations"][i]["str_name"] )
			mesh.get_buffer().prepare_buffer(GL_TRIANGLES, len(used_indices),GL_UNSIGNED_INT, mesh_data)
			mesh.get_buffer().create_buffer()
			mesh.set_informations(mesh_infos)
			mesh.set_aabb(data["bboxes"][0])
			mesh.assign_material("diffuse", data["mesh_informations"][i]["str_material"])

			meshes.append(mesh)


		return meshes
