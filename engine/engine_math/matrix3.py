
import math
from engine_math import vector3

#Note that we dont use any loops, to save some performance

class Matrix3:

	def __init__(self):
		self.m = [[1.0,0.0,0.0], [0.0,1.0,0.0], [0.0,0.0,1.0]]


	def get_values(self):
		return self.m


	def as_single_array(self):
		a = self.m

		return [
			a[0][0],
			a[0][1],
			a[0][2],

			a[1][0],
			a[1][1],
			a[1][2],

			a[2][0],
			a[2][1],
			a[2][2],

		]

	def set_identity(self):

		a = self.m

		a[0][0] = 1.0
		a[0][1] = 0.0
		a[0][2] = 0.0

		a[1][0] = 0.0
		a[1][1] = 1.0
		a[1][2] = 0.0

		a[2][0] = 0.0
		a[2][1] = 0.0
		a[2][2] = 1.0



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


	def get_x_vector(self):
		return vector3.Vector3(self.m[0][0], self.m[1][0], self.m[2][0])

	def get_y_vector(self):
		return vector3.Vector3(self.m[0][1], self.m[1][1], self.m[2][1])

	def get_z_vector(self):
		return vector3.Vector3(self.m[0][2], self.m[1][2], self.m[2][2])

	def set_rotation_x(self, angle):

		result_sin = math.sin(angle)
		result_cos = math.cos(angle)

		self.m[1][1] = result_cos
		self.m[2][1] =-result_sin

		self.m[1][2] = result_sin
		self.m[2][2] = result_cos

	def set_rotation_y(self, angle):

		result_sin = math.sin(angle)
		result_cos = math.cos(angle)

		self.m[0][0] = result_cos
		self.m[2][0] = result_sin

		self.m[0][2] =-result_sin
		self.m[2][2] = result_cos


	def set_rotation_z(self, angle):

		result_sin = math.sin(angle)
		result_cos = math.cos(angle)

		self.m[0][0] = result_cos
		self.m[1][0] =-result_sin

		self.m[0][1] = result_sin
		self.m[1][1] = result_cos


	def set_look_matrix(self, direction, up_vector = vector3.Vector3(0.0,1.0,0.0)):
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


	def mul_vec3(self, vector):
		result = vector3.Vector3()

		result.x = self.m[0][0] * vector.x + self.m[1][0] * vector.y + self.m[2][0] * vector.z
		result.y = self.m[0][1] * vector.x + self.m[1][1] * vector.y + self.m[2][1] * vector.z
		result.z = self.m[0][2] * vector.x + self.m[1][2] * vector.y + self.m[2][2] * vector.z

		return result

	def transpose(self):

		for x in range(0,3):
			for y in range(0,3):
				self.m[x][y] = self.m[y][x]

	def get_transpose(self):
		result = Matrix4()

		for x in range(0,3):
			for y in range(0,3):
				result.m[x][y] = self.m[y][x]

		return result

	def get_inverse(self):
		m = self.m
		r = Matrix3()

		determinat =    m[0][0] * m[1][1] * m[2][2] +\
						m[0][1] * m[1][2] * m[2][0] +\
						m[0][2] * m[1][0] * m[2][1] -\
						m[0][2] * m[1][1] * m[2][0] -\
						m[0][1] * m[1][0] * m[2][2] -\
						m[0][0] * m[1][2] * m[2][1]

		if determinat == 0.0:
			print("Warning, tried to inverse 3x3 Matrix with determinat zero")
			print(self)

			return self

		inv_determinat = 1.0 / determinat

		r.m[0][0] =  (m[1][1] * m[2][2] - m[1][2] * m[2][1]) * inv_determinat
		r.m[1][0] = -(m[1][0] * m[2][2] - m[1][2] * m[2][0]) * inv_determinat
		r.m[2][0] =  (m[1][0] * m[2][1] - m[1][1] * m[2][0]) * inv_determinat

		r.m[0][1] = -(m[0][1] * m[2][2] - m[0][2] * m[2][1]) * inv_determinat
		r.m[1][1] =  (m[0][0] * m[2][2] - m[0][2] * m[2][0]) * inv_determinat
		r.m[2][1] = -(m[0][0] * m[2][1] - m[0][1] * m[2][0]) * inv_determinat

		r.m[0][2] =  (m[0][1] * m[1][2] - m[0][2] * m[1][1]) * inv_determinat
		r.m[1][2] = -(m[0][0] * m[1][2] - m[0][2] * m[1][0]) * inv_determinat
		r.m[2][2] =  (m[0][0] * m[1][1] - m[0][1] * m[1][0]) * inv_determinat

		return r


	@staticmethod
	def interpolate(m1, m2, p):

		inv = (1.0 - p)
		r = Matrix4()
		a = m1.m
		b = m2.m

		r.m[0][0] = a[0][0] * inv + b[0][0] * p
		r.m[0][1] = a[0][1] * inv + b[0][1] * p
		r.m[0][2] = a[0][2] * inv + b[0][2] * p

		r.m[1][0] = a[1][0] * inv + b[1][0] * p
		r.m[1][1] = a[1][1] * inv + b[1][1] * p
		r.m[1][2] = a[1][2] * inv + b[1][2] * p

		r.m[2][0] = a[2][0] * inv + b[2][0] * p
		r.m[2][1] = a[2][1] * inv + b[2][1] * p
		r.m[2][2] = a[2][2] * inv + b[2][2] * p

		return r

	@staticmethod
	def from_rotation(rot):

		angle, axis = rot.get_angle_axis()
		len = axis.getLength()

		if len == 0:
			return Matrix3.get_identiy_matrix()

		m = Matrix3()

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

		return m

	#only uses the rotation part
	@staticmethod
	def from_matrix3x4(c):
		m = Matrix3()

		m.m[0][0] = c.m[0][0]
		m.m[0][1] = c.m[0][1]
		m.m[0][2] = c.m[0][2]

		m.m[1][0] = c.m[1][0]
		m.m[1][1] = c.m[1][1]
		m.m[1][2] = c.m[1][2]

		m.m[2][0] = c.m[2][0]
		m.m[2][1] = c.m[2][1]
		m.m[2][2] = c.m[2][2]

		return m


	def __mul__(self, other):
		result = Matrix3()
		a = self.m
		b = other.m
		c = result.m

		c[0][0] = a[0][0] * b[0][0] + a[1][0] * b[0][1] + a[2][0] * b[0][2]
		c[1][0] = a[0][0] * b[1][0] + a[1][0] * b[1][1] + a[2][0] * b[1][2]
		c[2][0] = a[0][0] * b[2][0] + a[1][0] * b[2][1] + a[2][0] * b[2][2]

		c[0][1] = a[0][1] * b[0][0] + a[1][1] * b[0][1] + a[2][1] * b[0][2]
		c[1][1] = a[0][1] * b[1][0] + a[1][1] * b[1][1] + a[2][1] * b[1][2]
		c[2][1] = a[0][1] * b[2][0] + a[1][1] * b[2][1] + a[2][1] * b[2][2]

		c[0][2] = a[0][2] * b[0][0] + a[1][2] * b[0][1] + a[2][2] * b[0][2]
		c[1][2] = a[0][2] * b[1][0] + a[1][2] * b[1][1] + a[2][2] * b[1][2]
		c[2][2] = a[0][2] * b[2][0] + a[1][2] * b[2][1] + a[2][2] * b[2][2]

		return result

	def __repr__(self):

		result = ""

		for x in range(0,3):
			for y in range(0,3):
				result = result + "[" + str( round( self.m[y][x], 4) ).ljust(8, '0')[0:8] + "]"

			result = result + "\n"


		return result + "\n"
