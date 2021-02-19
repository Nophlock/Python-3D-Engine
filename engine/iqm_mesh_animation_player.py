
from vector3		import Vector3
from matrix3x4 		import Matrix3x4
from transform 		import Transform
from quaternion 	import Quaternion


#https://github.com/ioquake/ioq3/blob/11337c9fa2fa45371182603863164a9186ff2b9e/code/renderergl2/tr_model_iqm.c for match
class IQMMeshAnimationPlayer:

	def __init__(self, meshes, mesh_data):
		self.meshes = meshes
		self.mesh_data = mesh_data
		self.anim_data = self.mesh_data["animation_data"]

		self.animations = {}
		self.bones = {}
		self.anim_matrices = []

		self.joint_matrices = []
		self.joint_inverse_matrices = []
		self.frame_matrices = []

		self.current_animation = ""
		self.animation_time = 0.0
		self.animation_speed = 1.0

		for i in range(100):
			self.anim_matrices.append(Matrix3x4() )

		self.prepare_data()

	def is_root(self, mesh_root):
		return self.meshes[0] == mesh_root

	#note that we're using a 3x4 matric, since its uses less space, needs less operation (4 per matrices) and its faster to invert
	def build_matrix(self, position, rotation, scale):

		matrix = Matrix3x4.from_matrix4(rotation.to_matrix4())

		matrix.scale(scale.x, scale.y, scale.z)
		matrix.set_translation(position.x, position.y, position.z)

		return matrix


	def prepare_data(self):


		for i in range(len(self.anim_data["animations"])):
			self.animations[self.anim_data["animations"][i]["name"]] = self.anim_data["animations"][i]


		for i in range(len(self.anim_data["joints"])):
			c_joint = self.anim_data["joints"][i]
			joint_matrix = self.build_matrix(c_joint["translate"], c_joint["rotate"], c_joint["scale"])
			inv_joint_matrix = joint_matrix.get_inverse()

			if c_joint["parent"] >= 0:
				joint_matrix = self.joint_matrices[ c_joint["parent"] ] * joint_matrix
				inv_joint_matrix = inv_joint_matrix * self.joint_inverse_matrices[ c_joint["parent"] ]

			self.joint_matrices.append(joint_matrix)
			self.joint_inverse_matrices.append(inv_joint_matrix)




		for i in range(len(self.anim_data["frame_positions"]) ):
			self.frame_matrices.append([])

			for j in range(len(self.anim_data["poses"])):

				pose = self.anim_data["joints"][j]
				frame_data = self.anim_data["frame_positions"][i][j]

				frame_matrix = self.build_matrix(frame_data["translate"], frame_data["rotate"], frame_data["scale"])

				if pose["parent"] >= 0:
					self.frame_matrices[i].append( self.joint_matrices[ pose["parent"] ] * frame_matrix * self.joint_inverse_matrices[j] )
				else:
					self.frame_matrices[i].append( frame_matrix * self.joint_inverse_matrices[j] )



	def play_animation(self, anim_name, play_speed):

		if anim_name not in self.animations:
			print("MeshAnimationPlayer: couldnt find animation: ", anim_name)
			return

		self.current_animation = anim_name
		self.animation_time = 0.0
		self.animation_speed = play_speed


	def get_all_aabbs(self):
		return self.mesh_data["bboxes"]

	def update(self, dt):

		if self.current_animation == "":
			return

		c_anim = self.animations[self.current_animation]
		bounds = (c_anim["first_frame"], c_anim["first_frame"] + c_anim["num_frames"])

		base_frame = int(self.animation_time)
		next_frame = base_frame + 1

		if next_frame >= bounds[1]-1:
			next_frame = 0

		self.animation_time = self.animation_time + self.animation_speed * c_anim["framerate"] * dt
		time_between = 	self.animation_time - float(base_frame)

		if self.animation_time >= bounds[1]-1:
			self.animation_time = bounds[0]

		#TODO: maybe we should interpolate from the current aabb to the next one, just like in the matrices. But is it worth the performance costs?
		for i in range(len(self.meshes)):
			self.meshes[i].set_aabb(self.mesh_data["bboxes"][base_frame])


		self.calculate_matrices(base_frame, next_frame, time_between)


	def calculate_matrices(self, base_frame, next_frame, time_between):


		for i in range( len(self.anim_data["frame_positions"][base_frame]) ):

			joint = self.anim_data["joints"][i]

			c_frame_matrix = self.frame_matrices[base_frame][i]
			c_target_frame_matrix = self.frame_matrices[next_frame][i]

			result = Matrix3x4.interpolate(c_frame_matrix, c_target_frame_matrix, time_between)

			if joint["parent"] >= 0:
				self.anim_matrices[i] = self.anim_matrices[joint["parent"]] * result
			else:
				self.anim_matrices[i] = result

			#self.bones[joint["name"]] = self.anim_matrices[i] #create a lookup table for the bones so we can attach stuff to it


	def get_animation_names(self):
		return self.animations.keys()


	def get_animation_matrices(self):
		return self.anim_matrices
