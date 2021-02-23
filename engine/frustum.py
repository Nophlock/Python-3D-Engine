

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



 	#by doing this, we risk some wrong results if the aabb is for example super large so that the corners arent in the frustum
	#but the face itself is inside of it so todo: check if theres an other way that isnt performance heavy
	def is_aabb_inside_frustum(self, aabb):

		knots = aabb.get_transformed_knots()

		for i in range(len(knots)):

			if self.is_point_inside_frustum(knots[i]):
				return True

		return False

	#if the point is outside of one planes it cant be inside the frustum itself
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
