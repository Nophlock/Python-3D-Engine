
from engine_math import vector3
from engine_math import matrix4

from transform	import Transform

class Camera(Transform):

	def __init__(self, engine_ref):
		super().__init__()

		self.engine				= engine_ref
		self.inverse_matrix		= matrix4.Matrix4()
		self.perspective_matrix = matrix4.Matrix4()
		self.inv_perspective_matrix = matrix4.Matrix4()
		self.fov = 0

		self.inverse_matrix.set_identity()
		self.perspective_matrix.set_identity()

	#derived from transform, needs to be adjusted
	def rebuild_matrix(self):
		self.result_matrix	= self.rotation_matrix * self.position_matrix
		self.inverse_matrix	= self.result_matrix.get_rt_inverse_matrix()
		self.need_update	= False

		if self.parent != None:
			self.result_matrix = self.parent.get_transformation_matrix() * self.result_matrix

		for child in self.childs:
			child.rebuild_matrix()

	#derived from transform, needs to be adjusted
	def set_local_position(self,position):
		self.position = position
		self.position_matrix.set_translation(-position.x, -position.y, -position.z)

		self.need_update = True


	def get_parent_matrix(self):
		return self.inverse_matrix


	# https://antongerdelan.net/opengl/raycasting.html
	def get_mouse_direction(self):
		mx,my = self.key_mapper.get_mouse_position()
		width,height = self.engine.get_size()

		nx = mx / width
		ny = my / height

		nx = nx * 2.0 - 1.0
		ny = ny * 2.0 - 1.0

		ray_clip = vector3.Vector3(nx,ny, -1.0)

		ray_eye = self.inv_perspective_matrix.mul_vec3(ray_clip, 1.0)
		ray_eye.z = -1.0

		ray_world = self.inverse_matrix.mul_vec3(ray_eye, 0.0)

		return ray_world





	def set_perspective_matrix(self, fov, aspect, near_plane, far_plane):
		self.fov = fov
		self.perspective_matrix.set_perspective_matrix(fov, aspect, near_plane, far_plane)
		self.inv_perspective_matrix = self.perspective_matrix.get_inverse()


	def get_perspective_matrix(self):
		return self.perspective_matrix
