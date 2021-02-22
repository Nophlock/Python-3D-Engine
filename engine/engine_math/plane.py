
from engine_math import vector3


class Plane:

	def __init__(self, normal,distance):
		self.normal 	= normal
		self.distance	= distance

	def normalize(self):
		self.normal.normalize()

	def get_distance(self, point):
		return self.normal.dot(point) + self.distance


	def get_inverse(self):
		return Plane(self.normal.inverse(), d)

	def is_ray_inside_plane(self, ray_start, ray_dir):

		if ray_dir.dot(self.normal) > 0:
			return False

		t = -(ray_start.dot(self.normal) + self.distance) / ray_dir.dot(normal)
		point = ray_start + ray_dir * t

		return True,t,point
