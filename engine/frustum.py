

from engine_math import vector3
from engine_math import matrix4
from engine_math import plane


class Frustum:

	def __init__(self):
		self.planes = []


	#must be the camera matrix mutliplied with the projection matrix
	def extract_frustum_planes(self, matrix):

		self.planes = []
		m = matrix.m

		#left plane
		a = m[0][3] + m[0][0]
		b = m[1][3] + m[1][0]
		c = m[2][3] + m[2][0]
		d = m[3][3] + m[3][0]

		self.planes.append( plane.Plane(vector3.Vector3(a,b,c), d) )

		#right plane
		a = m[0][3] - m[0][0]
		b = m[1][3] - m[1][0]
		c = m[2][3] - m[2][0]
		d = m[3][3] - m[3][0]

		self.planes.append( plane.Plane(vector3.Vector3(a,b,c), d) )

		#top plane
		a = m[0][3] + m[0][1]
		b = m[1][3] + m[1][1]
		c = m[2][3] + m[2][1]
		d = m[3][3] + m[3][1]

		self.planes.append( plane.Plane(vector3.Vector3(a,b,c), d) )

		#bottom plane
		a = m[0][3] - m[0][1]
		b = m[1][3] - m[1][1]
		c = m[2][3] - m[2][1]
		d = m[3][3] - m[3][1]

		self.planes.append( plane.Plane(vector3.Vector3(a,b,c), d) )

		#near plane
		a = m[0][3] + m[0][2]
		b = m[1][3] + m[1][2]
		c = m[2][3] + m[2][2]
		d = m[3][3] + m[3][2]

		self.planes.append( plane.Plane(vector3.Vector3(a,b,c), d) )

		#bottom plane
		a = m[0][3] - m[0][2]
		b = m[1][3] - m[1][2]
		c = m[2][3] - m[2][2]
		d = m[3][3] - m[3][2]

		self.planes.append( plane.Plane(vector3.Vector3(a,b,c), d) )

		#fixme maybe normalize all planes



	#todo: This knot stuff actually takes a lot of allocation in the same frame, we should cache it and use the data instead
	def is_aabb_inside_frustum(self, aabb):

		min,max = aabb.get_unprojected_min_max()

		knots = []

		knots.append(vector3.Vector3(min.x, min.y, min.z)) #000
		knots.append(vector3.Vector3(min.x, min.y, max.z)) #001
		knots.append(vector3.Vector3(min.x, max.y, min.z)) #010
		knots.append(vector3.Vector3(min.x, max.y, max.z)) #011
		knots.append(vector3.Vector3(max.x, min.y, min.z)) #100
		knots.append(vector3.Vector3(max.x, min.y, max.z)) #101
		knots.append(vector3.Vector3(max.x, max.y, min.z)) #110
		knots.append(vector3.Vector3(max.x, max.y, max.z)) #111

		for i in range(len(knots)):

			if self.is_point_inside_frustum(knots[i]):
				return True

		return False

	def is_point_inside_frustum(self, position):

		for plane in self.planes:

			if plane.get_distance(position) <= 0:
				return False

		return True

	def is_sphere_inside_frustum(self, position, radius):


		for plane in self.planes:

			if plane.get_distance(position) < -radius:
				return False

		return True
