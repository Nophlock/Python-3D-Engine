

from vector3 	import Vector3
from matrix4	import Matrix4
from plane		import Plane


class Frustum:
	
	def __init__(self):
		self.planes = []
		pass
		
		
	#must be the camera matrix mutliplied with the projection matrix
	def extract_frustum_planes(self, matrix):
	
		self.planes = []
		#see http://www.txutxi.com/?p=444 for lookup
		
		#left plane
		a = matrix.m[0][0] + matrix[3][0]
		b = matrix.m[0][1] + matrix[3][1]
		c = matrix.m[0][2] + matrix[3][2]
		d = matrix.m[0][3] + matrix[3][3]
		
		self.planes.append( Plane(Vector3(a,b,c), d) )
		
		#right plane
		a = -matrix.m[0][0] + matrix[3][0]
		b = -matrix.m[0][1] + matrix[3][1]
		c = -matrix.m[0][2] + matrix[3][2]
		d = -matrix.m[0][3] + matrix[3][3]
		
		self.planes.append( Plane(Vector3(a,b,c), d) )
		
		#bottom plane
		a = matrix.m[1][0] + matrix[3][0]
		b = matrix.m[1][1] + matrix[3][1]
		c = matrix.m[1][2] + matrix[3][2]
		d = matrix.m[1][3] + matrix[3][3]
		
		self.planes.append( Plane(Vector3(a,b,c), d) )
		
		#top plane
		a = -matrix.m[1][0] + matrix[3][0]
		b = -matrix.m[1][1] + matrix[3][1]
		c = -matrix.m[1][2] + matrix[3][2]
		d = -matrix.m[1][3] + matrix[3][3]
		
		self.planes.append( Plane(Vector3(a,b,c), d) )
		
		#near plane
		a = matrix.m[2][0] + matrix[3][0]
		b = matrix.m[2][1] + matrix[3][1]
		c = matrix.m[2][2] + matrix[3][2]
		d = matrix.m[2][3] + matrix[3][3]
		
		self.planes.append( Plane(Vector3(a,b,c), d) )
		
		#bottom plane
		a = -matrix.m[2][0] + matrix[3][0]
		b = -matrix.m[2][1] + matrix[3][1]
		c = -matrix.m[2][2] + matrix[3][2]
		d = -matrix.m[2][3] + matrix[3][3]
		
		self.planes.append( Plane(Vector3(a,b,c), d) )
		
		#fixme maybe normalize all planes
		

		
		
	def is_bbox_inside_frustum(self, min_point, max_point):
	
		if(self.is_point_inside_frustum(min_point) == False):
			return False
		elif(self.is_point_inside_frustum(max_point) == False):
			return False
	
	
		return True
		
	def is_point_inside_frustum(self, position):
	
		for plane in self.planes:
			
			if(plane.getDistance(position) <= 0):
				return False
	
		return True
		
	def is_sphere_inside_frustum(self, position, radius):
	
	
		for plane in self.planes:
			
			if(plane.getDistance(position) < -radius):
				return False
	
		return True