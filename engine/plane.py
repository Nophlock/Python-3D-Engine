
from vector3 import Vector3


class Plane:
	
	def __init__(self, normal,distance):
		self.normal 	= normal
		self.distance	= distance
		
	#@staticmethod
	#def fromRay(self, origin, direction, point):
		
		
	def normalize(self):
		self.normal.normalize()
		
	def getDistance(self, point):
		return self.normal.dot(point) + self.distance
		
	
	def getInverse(self):
		return Plane(self.normal.inverse(), d)
		
	def isRayInsidePlane(self, ray_start, ray_dir):
	
		if(ray_dir.dot(self.normal) > 0):
			return False
			
		t 		= -(ray_start.dot(self.normal) + self.distance) / (ray_dir.dot(normal) )
		point	= ray_start + ray_dir * t
		
		return (t,point)