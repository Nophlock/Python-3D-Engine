import math

from engine_math import vector3
from engine_math import matrix4

#todo, maybe we should switch to x,y,z components instead of an vector3 for performance reasons

class Quaternion:

	def __init__(self, axis = vector3.Vector3(), w = 1.0):
		self.axis	= axis
		self.w 		= w



	def get_axis_quaternion(self):
		half_angle = self.w/2
		sin_angle  = math.sin(half_angle)

		self.axis.x = self.axis.x * sin_angle
		self.axis.y = self.axis.y * sin_angle
		self.axis.z = self.axis.z * sin_angle
		self.w      = math.cos(half_angle)

		return Quaternion(self.axis, self.w)


	def get_angle_axis(self):

		if self.w > 1.0 or self.w < -1.0:
			self.normalize()

		angle = 2.0 * math.acos(self.w)
		s = math.sqrt(1.0 - self.w * self.w)

		if s < 0.001:
			return angle, self.axis

		return angle, (self.axis / s)



	@staticmethod
	def from_axis(axis, w):
		return Quaternion(axis, w).get_axis_quaternion()

	@staticmethod
	def lookAt(direction, up_vector = vector3.Vector3(0.0,1.0,0.0) ):
		matrix = matrix4.Matrix4()
		matrix.set_Look_matrix(direction, up_vector)

		return Quaternion.fromMatrix(matrix)

	@staticmethod
	def fromEuler(pitch, yaw, roll):
		result = quaternion.Quaternion()

		p = pitch  * 0.5
		y = yaw    * 0.5
		r = roll   * 0.5

		sinp = math.sin(p);
		siny = math.sin(y);
		sinr = math.sin(r);
		cosp = math.cos(p);
		cosy = math.cos(y);
		cosr = math.cos(r);

		result.axis.x = sinr * cosp * cosy - cosr * sinp * siny;
		result.axis.y = cosr * sinp * cosy + sinr * cosp * siny;
		result.axis.z = cosr * cosp * siny - sinr * sinp * cosy;
		result.w      = cosr * cosp * cosy + sinr * sinp * siny;

		return result

	@staticmethod
	def fromMatrix(matrix):
		trace = matrix.m[0][0] + matrix.m[1][1] + matrix.m[2][2]

		if trace > 0.0:
			s 	= 0.5 / math.sqrt(trace + 1.0)
			m_w = 0.25 / s
			m_x = (matrix.m[1][2] - matrix.m[2][1]) * s
			m_y = (matrix.m[2][0] - matrix.m[0][2]) * s
			m_z = (matrix.m[0][1] - matrix.m[1][0]) * s
		else:
			if matrix.m[0][0] > matrix.m[1][1] and matrix.m[0][0] > matrix.m[2][2]:
				s 	= math.sqrt(1.0 + matrix.m[0][0] - matrix.m[1][1] - matrix.m[2][2]) * 2.0
				m_w = (matrix.m[1][2] - matrix.m[2][1]) / s
				m_x = 0.25 * s
				m_y = (matrix.m[1][0] + matrix.m[0][1]) / s
				m_z = (matrix.m[2][0] + matrix.m[0][2]) / s
			elif matrix.m[1][1] > matrix.m[2][2]:
				s 	= math.sqrt(1.0 + matrix.m[1][1] - matrix.m[0][0] - matrix.m[2][2]) * 2.0
				m_w = (matrix.m[2][0] - matrix.m[0][2]) / s
				m_x = (matrix.m[1][0] + matrix.m[0][1]) / s
				m_y = 0.25 * s
				m_z = (matrix.m[2][1] + matrix.m[1][2]) / s
			else:
				s 	= math.sqrt(1.0 + matrix.m[2][2] - matrix.m[0][0] - matrix.m[1][1]) * 2.0
				m_w = (matrix.m[0][1] - matrix.m[1][0] ) / s
				m_x = (matrix.m[2][0] + matrix.m[0][2] ) / s
				m_y = (matrix.m[2][1] + matrix.m[1][2] ) / s
				m_z = 0.25 * s



		return Quaternion(vector3.Vector3(m_x,m_y,m_z), m_w)

	def getLength(self):
		return math.sqrt( self.axis.x * self.axis.x + self.axis.y*self.axis.y + self.axis.z * self.axis.z + self.w*self.w)

	def normalize(self):
		length = self.getLength()

		if(length == 0):
			length = 1.0

		self.axis	= self.axis / length
		self.w		= self.w	/ length


	def getNormalized(self):
		length = self.getLength()

		if(length == 0):
			length = 1.0

		norm_axis 	= self.axis / length
		norm_w		= self.w    / length

		return Quaternion(norm_axis, norm_w)

	def get_normalized(self):
		length = self.getLength()

		if(length == 0):
			length = 1.0

		norm_axis 	= vector3.Vector3(self.axis.x / length, self.axis.y / length, self.axis.z / length)
		norm_w		= self.w    / length

		return Quaternion(norm_axis, norm_w)


	def get_conjugate(self):
		return Quaternion(self.axis.inverse(), self.w)


	def dot(self, other):
		return self.axis.dot(other.axis) + self.w * other.w

	def getDotLength(self):
		return self.dot(self)

	def lerp(self, factor):
		return self + ((other-self).scale(factor))

	def slerp(self, other, t):
		angle = self.dot(other)
		quat1 = self

		if angle < 0.0:
			quat1 = self.scale( -1.0 )
			angle = -angle

		if 1.0 - angle > 0.001:
			return self.lerp(other, t)

		angle 	= math.clamp( angle, -1.0, 1.0)
		theta 	= math.acos(angle) * t
		co_quat	= (other - self.scale(angle) )

		return self.scale(math.cos(theta)) + co_quat.scale(math.sin(theta))


	def mulVector(self, vec):

		n_w = -self.axis.x * vec.x - self.axis.y * vec.y - self.axis.z * vec.z
		n_x =  self.w	   * vec.x + self.axis.y * vec.z - self.axis.z * vec.y
		n_y =  self.w	   * vec.y + self.axis.z * vec.x - self.axis.x * vec.z
		n_z =  self.w	   * vec.z + self.axis.x * vec.y - self.axis.y * vec.x

		return Quaternion(vector3.Vector3(n_x,n_y,n_z), n_w)


	def __mul__(self, other):
		a = self
		b = other

		n_w = a.w * b.w 		- a.axis.x * b.axis.x 	- a.axis.y * b.axis.y - a.axis.z * b.axis.z
		n_x = a.w * b.axis.x 	+ a.axis.x * b.w 		+ a.axis.y * b.axis.z - a.axis.z * b.axis.y
		n_y = a.w * b.axis.y 	+ a.axis.y * b.w 		+ a.axis.z * b.axis.x - a.axis.x * b.axis.z
		n_z = a.w * b.axis.z 	+ a.axis.z * b.w 		+ a.axis.x * b.axis.y - a.axis.y * b.axis.x

		return Quaternion(vector3.Vector3(n_x,n_y,n_z), n_w)

	def __sub__(self, other):
		return Quaternion(self.axis - other.axis, self.w - other.w)

	def __add__(self, other):
		return Quaternion(self.axis + other.axis, self.w + other.w)

	def scale(self, val):
		return Quaternion(self.axis * val, self.w * val)

	def __repr__(self):
		return 'X = ' + str( round( self.axis.x, 4) ).ljust(8, '0')[0:8] + '\nY = ' + str( round( self.axis.y, 4) ).ljust(8, '0')[0:8] + '\nZ = ' + str( round( self.axis.z, 4) ).ljust(8, '0')[0:8] + '\nW = ' + str( round( self.w, 4) ).ljust(8, '0')[0:8] + '\n'


	#from https://paroj.github.io/gltut/Positioning/Tut08%20Quaternions.html
	def to_matrix4(self):
		result = matrix4.Matrix4()
		a = result.m

		xx = 2.0 * self.axis.x * self.axis.x
		xy = 2.0 * self.axis.x * self.axis.y
		xz = 2.0 * self.axis.x * self.axis.z
		xw = 2.0 * self.axis.x * self.w

		yy = 2.0 * self.axis.y * self.axis.y
		yz = 2.0 * self.axis.y * self.axis.z
		yw = 2.0 * self.axis.y * self.w

		zz = 2.0 * self.axis.z * self.axis.z
		zw = 2.0 * self.axis.z * self.w

		a[0][0] = 1.0 - yy - zz
		a[0][1] = xy+zw
		a[0][2] = xz-yw

		a[1][0] = xy - zw
		a[1][1] = 1.0 - xx - zz
		a[1][2] = yz + xw

		a[2][0] = xz + yw
		a[2][1] = yz - xw
		a[2][2] = 1.0 - xx - yy

		a[3][3] = 1.0

		return result
