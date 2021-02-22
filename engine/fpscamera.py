
from camera import Camera
from engine_math import quaternion
from engine_math import vector3

from pyglet.window import key
from pyglet.window import mouse

class FPSCamera(Camera):

	def __init__(self, engine_ref):
		super().__init__(engine_ref)

		self.movement_speed	= 10.0
		self.sensitive		= 0.01
		self.sensitive_x	= 0.0
		self.sensitive_y	= 0.0

		self.key_mapper = self.engine.get_key_mapper()


	def update(self, dt):
		self.process_key_input(dt)
		self.process_mouse_input(dt)

	def process_key_input(self,dt):

		if self.key_mapper.is_key_holded(key.W):

			forward = self.get_forward_vector()

			self.set_local_position( self.position - forward * self.movement_speed * dt)

		elif self.key_mapper.is_key_holded(key.S):

			forward = self.get_forward_vector()
			self.set_local_position( self.position + forward * self.movement_speed * dt)


		if self.key_mapper.is_key_holded(key.A):

			sideward = self.get_right_vector()
			self.set_local_position( self.position - sideward * self.movement_speed * dt)
		elif self.key_mapper.is_key_holded(key.D):

			sideward = self.get_right_vector()
			self.set_local_position( self.position + sideward * self.movement_speed * dt)


	def update_rotation_matrix(self):

		y_axis = quaternion.Quaternion.from_axis(vector3.Vector3.unit_y()	, self.sensitive_x)
		x_axis = quaternion.Quaternion.from_axis(vector3.Vector3.unit_x()	,-self.sensitive_y)

		self.rotation = self.rotation * y_axis
		self.rotation = x_axis * self.rotation
		self.rotation.normalize()
		self.rotation_matrix = self.rotation.to_matrix4()

		self.need_update = True

		self.sensitive_x = 0
		self.sensitive_y = 0


	def process_mouse_input(self, dt):

		meshes = self.engine.get_scene_manager().objects
		aabb = meshes[0].get_aabb()


		if self.key_mapper.is_key_holded("m_" + str(mouse.LEFT) ) :

			dx,dy = self.key_mapper.get_mouse_relative_position()
			self.engine.set_mouse_visible(False)

			self.sensitive_x = dx * self.sensitive
			self.sensitive_y = dy * self.sensitive

			self.update_rotation_matrix()

		if self.key_mapper.is_key_holded("m_" + str(mouse.RIGHT)):
			ray_pos = self.position
			ray_dir = self.get_mouse_direction()

			res, t_min, t_max = aabb.intersect_aabb_ray(self.engine.get_scene_manager().transform, ray_pos, ray_dir)

			print(res, t_min, t_max)


		if self.key_mapper.is_key_holded("m_" + str(mouse.MIDDLE)):
			print(self.frustum.is_aabb_inside_frustum(aabb))
