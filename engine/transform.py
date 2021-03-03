

from engine_math import vector3
from engine_math import matrix4
from engine_math import quaternion

class Transform:
	def __init__(self, entity = None):

		self.attached_entity = entity
		self.position 		= vector3.Vector3()
		self.rotation		= quaternion.Quaternion()
		self.scale			= vector3.Vector3()

		self.result_matrix	= matrix4.Matrix4()
		self.rotation_matrix= matrix4.Matrix4()
		self.position_matrix= matrix4.Matrix4()
		self.scale_matrix	= matrix4.Matrix4()


		self.need_update	= False
		self.childs			= []
		self.parent			= None

	def get_local_position(self):
		return self.position

	def set_local_position(self, position):
		self.position = position
		self.position_matrix.set_translation(position.x,position.y,position.z)

		self.need_update = True

	def set_local_scale(self, scale):
		self.scale = scale
		self.scale_matrix.set_scale(scale.x,scale.y,scale.z)

		self.need_update = True

	def set_local_rotation(self, rotation):
		self.rotation = rotation

		self.rotation_matrix	= self.rotation.to_matrix4()
		self.need_update		= True

	def get_local_rotation(self):
		return self.rotation

	def get_local_rotation_matrix(self):
		return self.rotation_matrix

	def look_at(self, direction, up_vector = vector3.Vector3(0.0,1.0,0.0) ):
		self.rotation_matrix.set_look_matrix(direction, up_vector)
		self.rotation 			= quaternion.Quaternion.from_matrix(self.rotation_matrix)
		self.rotation_matrix 	= self.rotation.to_matrix()

		self.need_update = True

	def get_forward_vector(self):
		return self.rotation_matrix.get_z_vector()

	def get_up_vector(self):
		return self.rotation_matrix.get_y_vector()

	def get_right_vector(self):
		return self.rotation_matrix.get_x_vector()

	def add_child(self, child):
		self.childs.append(child)
		child.parent = self

	def rebuild_matrix(self):
		self.result_matrix	= self.position_matrix * self.rotation_matrix * self.scale_matrix
		self.need_update	= False

		if self.parent != None:
			self.result_matrix = self.parent.get_parent_matrix() * self.result_matrix

		for child in self.childs:
			child.rebuild_matrix()

		if self.attached_entity != None:
			self.attached_entity.transform_was_modified()

	def get_parent_matrix(self):
		return self.get_transformation_matrix()

	def get_transformation_matrix(self):

		if self.need_update:
			self.rebuild_matrix()
		elif self.parent != None and self.parent.need_update:
			self.rebuild_matrix()

		return self.result_matrix
