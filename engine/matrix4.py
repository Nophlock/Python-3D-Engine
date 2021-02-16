
import math
from vector3 import Vector3

#Note that we dont use any loops, to save some performance

class Matrix4:

	def __init__(self):
		self.m = [[1.0,0.0,0.0,0.0], [0.0,1.0,0.0,0.0], [0.0,0.0,1.0,0.0], [0.0, 0.0, 0.0,0.0]]


	def getValues(self):
		return self.m


	def as_single_array(self):
		a = self.m

		return [
			a[0][0],
			a[0][1],
			a[0][2],
			a[0][3],

			a[1][0],
			a[1][1],
			a[1][2],
			a[1][3],

			a[2][0],
			a[2][1],
			a[2][2],
			a[2][3],

			a[3][0],
			a[3][1],
			a[3][2],
			a[3][3],
		]

	def set_identity(self):

		a = self.m

		a[0][0] = 1.0
		a[0][1] = 0.0
		a[0][2] = 0.0
		a[0][3] = 0.0

		a[1][0] = 0.0
		a[1][1] = 1.0
		a[1][2] = 0.0
		a[1][3] = 0.0

		a[2][0] = 0.0
		a[2][1] = 0.0
		a[2][2] = 1.0
		a[2][3] = 0.0

		a[3][0] = 0.0
		a[3][1] = 0.0
		a[3][2] = 0.0
		a[3][3] = 1.0

	def set_translation(self, x,y,z):
		self.m[3][0] = x
		self.m[3][1] = y
		self.m[3][2] = z

	def setTranslation(self, x,y,z):
		self.m[3][0] = x
		self.m[3][1] = y
		self.m[3][2] = z

	def setScalation(self, x,y,z):
		self.m[0][0] = x
		self.m[1][1] = y
		self.m[2][2] = z

	def set_scale(self, x,y,z):
		self.m[0][0] = x
		self.m[1][1] = y
		self.m[2][2] = z


	def scale(self, x,y,z):

		self.m[0][0] *= x
		self.m[1][0] *= x
		self.m[2][0] *= x

		self.m[0][1] *= y
		self.m[1][1] *= y
		self.m[2][1] *= y

		self.m[0][2] *= z
		self.m[1][2] *= z
		self.m[2][2] *= z

	#why is this transposed?
	def get_x_vector(self):
		return Vector3(self.m[0][0], self.m[1][0], self.m[2][0])

	def get_y_vector(self):
		return Vector3(self.m[0][1], self.m[1][1], self.m[2][1])

	def get_z_vector(self):
		return Vector3(self.m[0][2], self.m[1][2], self.m[2][2])

	def setRotationX(self, angle):

		result_sin = math.sin(angle)
		result_cos = math.cos(angle)

		self.m[1][1] = result_cos
		self.m[2][1] =-result_sin

		self.m[1][2] = result_sin
		self.m[2][2] = result_cos

	def setRotationY(self, angle):

		result_sin = math.sin(angle)
		result_cos = math.cos(angle)

		self.m[0][0] = result_cos
		self.m[2][0] = result_sin

		self.m[0][2] =-result_sin
		self.m[2][2] = result_cos


	def setRotationZ(self, angle):

		result_sin = math.sin(angle)
		result_cos = math.cos(angle)

		self.m[0][0] = result_cos
		self.m[1][0] =-result_sin

		self.m[0][1] = result_sin
		self.m[1][1] = result_cos

	#goes from the point, that the matrix is already in its identity form or a reused projection matrix
	def setPerspectiveMatrix(self, fov, aspect, near_plane, far_plane):
		range 		= far_plane - near_plane
		half_fov	= math.tan( math.radians( fov / 2.0 ) )

		self.m[0][0] = 1.0 / (half_fov * aspect)
		self.m[1][1] = 1.0 / (half_fov) #y axis is normalized

		self.m[2][2] = -(far_plane + near_plane) / range
		self.m[2][3] = -1.0

		self.m[3][2] = -(2.0 * far_plane * near_plane) / range
		self.m[3][3] = 0


	def setLookMatrix(self, direction, up_vector = Vector3(0.0,1.0,0.0)):
		z_axis	= direction
		z_axis.normalize()

		x_axis	= up_vector.cross( z_axis )
		x_axis.normalize()

		y_axis	= z_axis.cross(x_axis)

		self.m[0][0] = x_axis.x
		self.m[1][0] = x_axis.y
		self.m[2][0] = x_axis.z

		self.m[0][1] = y_axis.x
		self.m[1][1] = y_axis.y
		self.m[2][1] = y_axis.z

		self.m[0][2] = z_axis.x
		self.m[1][2] = z_axis.y
		self.m[2][2] = z_axis.z

		self.m[3][3] = 1.0


	def mul_vec3(self, vector, w = 1.0):
		result = Vector3()

		result.x = self.m[0][0] * vector.x + self.m[1][0] * vector.y + self.m[2][0] * vector.z + self.m[3][0] * w
		result.y = self.m[0][1] * vector.x + self.m[1][1] * vector.y + self.m[2][1] * vector.z + self.m[3][1] * w
		result.z = self.m[0][2] * vector.x + self.m[1][2] * vector.y + self.m[2][2] * vector.z + self.m[3][2] * w

		return result

	def transpose(self):

		for x in range(0,4):
			for y in range(0,4):
				self.m[x][y] = self.m[y][x]

	def get_transpose(self):
		result = Matrix4()

		for x in range(0,4):
			for y in range(0,4):
				result.m[x][y] = self.m[y][x]

		return result

	def getRotationMatrix(self):
		result = Matrix4()

		for x in range(0,3):
			for y in range(0,3):
				result.m[x][y] = self.m[x][y]

		return result

	def getTransposeRotationMatrix(self):
		result = Matrix4()

		for x in range(0,3):
			for y in range(0,3):
				result.m[x][y] = self.m[y][x]

		return result


	#fast inverse, finds solution as long the matrix is orthogonal( all columns are unit vectors )
	def get_rt_inverse_matrix(self):
		inverse_position	= Matrix4()
		inverse_rotation	= self.getTransposeRotationMatrix()

		inverse_position.setTranslation( -self.m[3][0], -self.m[3][1], -self.m[3][2] )

		return inverse_rotation*inverse_position



	#normal inverse, finds solution as long determinat is != 0
	def get_inverse(self):

		result = Matrix4()
		result.m[0][0] = self.m[1][1] * self.m[2][2] * self.m[3][3] -\
						 self.m[1][1] * self.m[2][3] * self.m[3][2] -\
						 self.m[2][1] * self.m[1][2] * self.m[3][3] +\
						 self.m[2][1] * self.m[1][3] * self.m[3][2] +\
						 self.m[3][1] * self.m[1][2] * self.m[2][3] -\
						 self.m[3][1] * self.m[1][3] * self.m[2][2]

		result.m[1][0] =-self.m[1][0] * self.m[2][2] * self.m[3][3] +\
						 self.m[1][0] * self.m[2][3] * self.m[3][2] +\
						 self.m[2][0] * self.m[1][2] * self.m[3][3] -\
						 self.m[2][0] * self.m[1][3] * self.m[3][2] -\
						 self.m[3][0] * self.m[1][2] * self.m[2][3] +\
						 self.m[3][0] * self.m[1][3] * self.m[2][2]

		result.m[2][0] = self.m[1][0] * self.m[2][1] * self.m[3][3] -\
						 self.m[1][0] * self.m[2][3] * self.m[3][1] -\
						 self.m[2][0] * self.m[1][1] * self.m[3][3] +\
						 self.m[2][0] * self.m[1][3] * self.m[3][1] +\
						 self.m[3][0] * self.m[1][1] * self.m[2][3] -\
						 self.m[3][0] * self.m[1][3] * self.m[2][1]

		result.m[3][0] =-self.m[1][0] * self.m[2][1] * self.m[3][2] +\
						 self.m[1][0] * self.m[2][2] * self.m[3][1] +\
						 self.m[2][0] * self.m[1][1] * self.m[3][2] -\
						 self.m[2][0] * self.m[1][2] * self.m[3][1] -\
						 self.m[3][0] * self.m[1][1] * self.m[2][2] +\
						 self.m[3][0] * self.m[1][2] * self.m[2][1]


		result.m[0][1] =-self.m[0][1] * self.m[2][2] * self.m[3][3] +\
						 self.m[0][1] * self.m[2][3] * self.m[3][2] +\
						 self.m[2][1] * self.m[0][2] * self.m[3][3] -\
						 self.m[2][1] * self.m[0][3] * self.m[3][2] -\
						 self.m[3][1] * self.m[0][2] * self.m[2][3] +\
						 self.m[3][1] * self.m[0][3] * self.m[2][2]

		result.m[1][1] = self.m[0][0] * self.m[2][2] * self.m[3][3] -\
						 self.m[0][0] * self.m[2][3] * self.m[3][2] -\
						 self.m[2][0] * self.m[0][2] * self.m[3][3] +\
						 self.m[2][0] * self.m[0][3] * self.m[3][2] +\
						 self.m[3][0] * self.m[0][2] * self.m[2][3] -\
						 self.m[3][0] * self.m[0][3] * self.m[2][2]

		result.m[2][1] =-self.m[0][0] * self.m[2][1] * self.m[3][3] +\
						 self.m[0][0] * self.m[2][3] * self.m[3][1] +\
						 self.m[2][0] * self.m[0][1] * self.m[3][3] -\
						 self.m[2][0] * self.m[0][3] * self.m[3][1] -\
						 self.m[3][0] * self.m[0][1] * self.m[2][3] +\
						 self.m[3][0] * self.m[0][3] * self.m[2][1]

		result.m[3][1] = self.m[0][0] * self.m[2][1] * self.m[3][2] -\
						 self.m[0][0] * self.m[2][2] * self.m[3][1] -\
						 self.m[2][0] * self.m[0][1] * self.m[3][2] +\
						 self.m[2][0] * self.m[0][2] * self.m[3][1] +\
						 self.m[3][0] * self.m[0][1] * self.m[2][2] -\
						 self.m[3][0] * self.m[0][2] * self.m[2][1]


		result.m[0][2] = self.m[0][1] * self.m[1][2] * self.m[3][3] -\
						 self.m[0][1] * self.m[1][3] * self.m[3][2] -\
						 self.m[1][1] * self.m[0][2] * self.m[3][3] +\
						 self.m[1][1] * self.m[0][3] * self.m[3][2] +\
						 self.m[3][1] * self.m[0][2] * self.m[1][3] -\
						 self.m[3][1] * self.m[0][3] * self.m[1][2]

		result.m[1][2] =-self.m[0][0] * self.m[1][2] * self.m[3][3] +\
						 self.m[0][0] * self.m[1][3] * self.m[3][2] +\
						 self.m[1][0] * self.m[0][2] * self.m[3][3] -\
						 self.m[1][0] * self.m[0][3] * self.m[3][2] -\
						 self.m[3][0] * self.m[0][2] * self.m[1][3] +\
						 self.m[3][0] * self.m[0][3] * self.m[1][2]


		result.m[2][2] = self.m[0][0] * self.m[1][1] * self.m[3][3] -\
						 self.m[0][0] * self.m[1][3] * self.m[3][1] -\
						 self.m[1][0] * self.m[0][1] * self.m[3][3] +\
						 self.m[1][0] * self.m[0][3] * self.m[3][1] +\
						 self.m[3][0] * self.m[0][1] * self.m[1][3] -\
						 self.m[3][0] * self.m[0][3] * self.m[1][1]


		result.m[3][2] =-self.m[0][0] * self.m[1][1] * self.m[3][2] +\
						 self.m[0][0] * self.m[1][2] * self.m[3][1] +\
						 self.m[1][0] * self.m[0][1] * self.m[3][2] -\
						 self.m[1][0] * self.m[0][2] * self.m[3][1] -\
						 self.m[3][0] * self.m[0][1] * self.m[1][2] +\
						 self.m[3][0] * self.m[0][2] * self.m[1][1]


		result.m[0][3] =-self.m[0][1] * self.m[1][2] * self.m[2][3] +\
						 self.m[0][1] * self.m[1][3] * self.m[2][2] +\
						 self.m[1][1] * self.m[0][2] * self.m[2][3] -\
						 self.m[1][1] * self.m[0][3] * self.m[2][2] -\
						 self.m[2][1] * self.m[0][2] * self.m[1][3] +\
						 self.m[2][1] * self.m[0][3] * self.m[1][2]


		result.m[1][3] = self.m[0][0] * self.m[1][2] * self.m[2][3] -\
						 self.m[0][0] * self.m[1][3] * self.m[2][2] -\
						 self.m[1][0] * self.m[0][2] * self.m[2][3] +\
						 self.m[1][0] * self.m[0][3] * self.m[2][2] +\
						 self.m[2][0] * self.m[0][2] * self.m[1][3] -\
						 self.m[2][0] * self.m[0][3] * self.m[1][2]


		result.m[2][3] =-self.m[0][0] * self.m[1][1] * self.m[2][3] +\
						 self.m[0][0] * self.m[1][3] * self.m[2][1] +\
						 self.m[1][0] * self.m[0][1] * self.m[2][3] -\
						 self.m[1][0] * self.m[0][3] * self.m[2][1] -\
						 self.m[2][0] * self.m[0][1] * self.m[1][3] +\
						 self.m[2][0] * self.m[0][3] * self.m[1][1]


		result.m[3][3] = self.m[0][0] * self.m[1][1] * self.m[2][2] -\
						 self.m[0][0] * self.m[1][2] * self.m[2][1] -\
						 self.m[1][0] * self.m[0][1] * self.m[2][2] +\
						 self.m[1][0] * self.m[0][2] * self.m[2][1] +\
						 self.m[2][0] * self.m[0][1] * self.m[1][2] -\
						 self.m[2][0] * self.m[0][2] * self.m[1][1]

		determinate = 	self.m[0][0] * result.m[0][0] +\
						self.m[0][1] * result.m[1][0] +\
						self.m[0][2] * result.m[2][0] +\
						self.m[0][3] * result.m[3][0]

		if determinate == 0.0:
			print("Warning, matrix has no determinat")
			return self

		determinate = 1.0 / determinate

		result.m[0][0] = result.m[0][0] * determinate
		result.m[0][1] = result.m[0][1] * determinate
		result.m[0][2] = result.m[0][2] * determinate
		result.m[0][3] = result.m[0][3] * determinate

		result.m[1][0] = result.m[1][0] * determinate
		result.m[1][1] = result.m[1][1] * determinate
		result.m[1][2] = result.m[1][2] * determinate
		result.m[1][3] = result.m[1][3] * determinate

		result.m[2][0] = result.m[2][0] * determinate
		result.m[2][1] = result.m[2][1] * determinate
		result.m[2][2] = result.m[2][2] * determinate
		result.m[2][3] = result.m[2][3] * determinate

		result.m[3][0] = result.m[3][0] * determinate
		result.m[3][1] = result.m[3][1] * determinate
		result.m[3][2] = result.m[3][2] * determinate
		result.m[3][3] = result.m[3][3] * determinate

		return result


	@staticmethod
	def interpolate(m1, m2, p):

		inv = (1.0 - p)
		r = Matrix4()
		a = m1.m
		b = m2.m

		r.m[0][0] = a[0][0] * inv + b[0][0] * p
		r.m[0][1] = a[0][1] * inv + b[0][1] * p
		r.m[0][2] = a[0][2] * inv + b[0][2] * p
		r.m[0][3] = a[0][3] * inv + b[0][3] * p

		r.m[1][0] = a[1][0] * inv + b[1][0] * p
		r.m[1][1] = a[1][1] * inv + b[1][1] * p
		r.m[1][2] = a[1][2] * inv + b[1][2] * p
		r.m[1][3] = a[1][3] * inv + b[1][3] * p

		r.m[2][0] = a[2][0] * inv + b[2][0] * p
		r.m[2][1] = a[2][1] * inv + b[2][1] * p
		r.m[2][2] = a[2][2] * inv + b[2][2] * p
		r.m[2][3] = a[2][3] * inv + b[2][3] * p

		r.m[3][0] = a[3][0] * inv + b[3][0] * p
		r.m[3][1] = a[3][1] * inv + b[3][1] * p
		r.m[3][2] = a[3][2] * inv + b[3][2] * p
		r.m[3][3] = a[3][3] * inv + b[3][3] * p

		return r

	@staticmethod
	def from_rotation(rot):

		angle, axis = rot.get_angle_axis()
		len = axis.getLength()

		if len == 0:
			return Matrix4.get_identiy_matrix()

		m = Matrix4()

		x = axis.x / len
		y = axis.y / len
		z = axis.z / len

		c = math.cos(angle)
		s = math.sin(angle)

		m.m[0][0] = x*x*(1-c)+c
		m.m[0][1] = x*y*(1-c)+z*s
		m.m[0][2] = x*z*(1-c)-y*s

		m.m[1][0] = y*x*(1-c)-z*s
		m.m[1][1] = y*y*(1-c)+c
		m.m[1][2] = y*z*(1-c)+x*s

		m.m[2][0] = z*x*(1-c)+y*s
		m.m[2][1] = z*y*(1-c)-x*s
		m.m[2][2] = z*z*(1-c)+c

		m.m[3][3] = 1.0


		return m

	@staticmethod
	def from_matrix3x4(c):
		m = Matrix4()

		m.m[0][0] = c.m[0][0]
		m.m[0][1] = c.m[0][1]
		m.m[0][2] = c.m[0][2]

		m.m[1][0] = c.m[1][0]
		m.m[1][1] = c.m[1][1]
		m.m[1][2] = c.m[1][2]

		m.m[2][0] = c.m[2][0]
		m.m[2][1] = c.m[2][1]
		m.m[2][2] = c.m[2][2]

		m.m[3][0] = c.m[3][0]
		m.m[3][1] = c.m[3][1]
		m.m[3][2] = c.m[3][2]

		m.m[3][3] = 1.0

		return m


	def __mul__(self, other):
		result = Matrix4()
		a = self.m
		b = other.m
		c = result.m

		c[0][0] = a[0][0] * b[0][0] + a[1][0] * b[0][1] + a[2][0] * b[0][2] + a[3][0] * b[0][3]
		c[1][0] = a[0][0] * b[1][0] + a[1][0] * b[1][1] + a[2][0] * b[1][2] + a[3][0] * b[1][3]
		c[2][0] = a[0][0] * b[2][0] + a[1][0] * b[2][1] + a[2][0] * b[2][2] + a[3][0] * b[2][3]
		c[3][0] = a[0][0] * b[3][0] + a[1][0] * b[3][1] + a[2][0] * b[3][2] + a[3][0] * b[3][3]

		c[0][1] = a[0][1] * b[0][0] + a[1][1] * b[0][1] + a[2][1] * b[0][2] + a[3][1] * b[0][3]
		c[1][1] = a[0][1] * b[1][0] + a[1][1] * b[1][1] + a[2][1] * b[1][2] + a[3][1] * b[1][3]
		c[2][1] = a[0][1] * b[2][0] + a[1][1] * b[2][1] + a[2][1] * b[2][2] + a[3][1] * b[2][3]
		c[3][1] = a[0][1] * b[3][0] + a[1][1] * b[3][1] + a[2][1] * b[3][2] + a[3][1] * b[3][3]

		c[0][2] = a[0][2] * b[0][0] + a[1][2] * b[0][1] + a[2][2] * b[0][2] + a[3][2] * b[0][3]
		c[1][2] = a[0][2] * b[1][0] + a[1][2] * b[1][1] + a[2][2] * b[1][2] + a[3][2] * b[1][3]
		c[2][2] = a[0][2] * b[2][0] + a[1][2] * b[2][1] + a[2][2] * b[2][2] + a[3][2] * b[2][3]
		c[3][2] = a[0][2] * b[3][0] + a[1][2] * b[3][1] + a[2][2] * b[3][2] + a[3][2] * b[3][3]

		c[0][3] = a[0][3] * b[0][0] + a[1][3] * b[0][1] + a[2][3] * b[0][2] + a[3][3] * b[0][3]
		c[1][3] = a[0][3] * b[1][0] + a[1][3] * b[1][1] + a[2][3] * b[1][2] + a[3][3] * b[1][3]
		c[2][3] = a[0][3] * b[2][0] + a[1][3] * b[2][1] + a[2][3] * b[2][2] + a[3][3] * b[2][3]
		c[3][3] = a[0][3] * b[3][0] + a[1][3] * b[3][1] + a[2][3] * b[3][2] + a[3][3] * b[3][3]

		return result

	def __repr__(self):

		result = ""

		for x in range(0,4):
			for y in range(0,4):
				result = result + "[" + str( round( self.m[y][x], 4) ).ljust(8, '0')[0:8] + "]"

			result = result + "\n"


		return result + "\n"
