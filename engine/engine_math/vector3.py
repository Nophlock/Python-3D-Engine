import math


class Vector3:

	def __init__(self, x = 0.0,y = 0.0,z = 0.0):
		self.x = x
		self.y = y
		self.z = z

	@staticmethod
	def unit_x():
		return Vector3(1.0,0.0,0.0)

	@staticmethod
	def unit_y():
		return Vector3(0.0,1.0,0.0)

	@staticmethod
	def unit_z():
		return Vector3(0.0,0.0,1.0)


	@staticmethod
	def lerp(a,b, p):
		return a + (b-a) * p


	def unpack(self):
		return (self.x, self.y, self.z)

	def dot(self, other):
		return self.x * other.x + self.y * other.y + self.z * other.z

	def cross(self, other):
		return Vector3( self.y * other.z - self.z * other.y,
						self.z * other.x - self.x * other.z,
						self.x * other.y - self.y * other.x  )

	def negate(self):
		return Vector3(-self.x, -self.y, -self.z)

	def get_len(self):
		return math.sqrt( self.x*self.x + self.y*self.y + self.z*self.z)

	def normalize(self):
		length = self.getLength()

		if length == 0:
			length = 1

		self.x = self.x / length
		self.y = self.y / length
		self.z = self.z / length

	def get_normalized(self):
		length = self.get_len()
		return Vector3( self.x / length, self.y / length, self.z / length )

	def __repr__(self):
		return "(" + str(round(self.x, 3)) + "," + str(round(self.y,3)) + "," + str(round(self.z,3)) + ")"

	def __add__(self, other):
		return Vector3( self.x + other.x, self.y + other.y, self.z + other.z)

	def __sub__(self, other):
		return Vector3( self.x - other.x, self.y - other.y, self.z - other.z)

	def __mul__(self, other):
		return Vector3( self.x * other, self.y * other, self.z * other)

	def __floordiv__(self, other):
		return Vector3(self.x / other, self.y / other, self.z / other)

	def __truediv__(self, other):
		return Vector3(self.x / other, self.y / other, self.z / other)

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y and self.z == other.z

	def __ne__(self, other):
		return not self.__eq__(other)
