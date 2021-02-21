

import math

from engine_math import vector3
from engine_math import matrix4

#https://github.com/ioquake/ioq3/blob/11337c9fa2fa45371182603863164a9186ff2b9e/code/renderergl2/tr_model_iqm.c

#https://github.com/urho3d/Urho3D/blob/master/Source/Urho3D/Math/Matrix3x4.h
#https://github.com/urho3d/Urho3D/blob/master/Source/Urho3D/Math/Matrix3x4.cpp

class Matrix3x4:

    def __init__(self):
    	self.m = [[1.0,0.0,0.0], [0.0,1.0,0.0], [0.0,0.0,1.0], [0.0, 0.0, 0.0]]


    @staticmethod
    def from_matrix4(c):
        m = Matrix3x4()
        b = c.m

        m.m[0][0] = b[0][0]
        m.m[0][1] = b[0][1]
        m.m[0][2] = b[0][2]

        m.m[1][0] = b[1][0]
        m.m[1][1] = b[1][1]
        m.m[1][2] = b[1][2]

        m.m[2][0] = b[2][0]
        m.m[2][1] = b[2][1]
        m.m[2][2] = b[2][2]

        m.m[3][0] = b[3][0]
        m.m[3][1] = b[3][1]
        m.m[3][2] = b[3][2]

        return m


    def set_translation(self, x,y,z):
        self.m[3][0] = x
        self.m[3][1] = y
        self.m[3][2] = z

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


    def get_inverse(self):

        m = self.m
        r = Matrix3x4()

        determinat =    m[0][0] * m[1][1] * m[2][2] +\
                        m[0][1] * m[1][2] * m[2][0] +\
                        m[0][2] * m[1][0] * m[2][1] -\
                        m[0][2] * m[1][1] * m[2][0] -\
                        m[0][1] * m[1][0] * m[2][2] -\
                        m[0][0] * m[1][2] * m[2][1]

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

        r.m[3][0] = -(m[3][0] * r.m[0][0] + m[3][1] * r.m[1][0] + m[3][2] * r.m[2][0])
        r.m[3][1] = -(m[3][0] * r.m[0][1] + m[3][1] * r.m[1][1] + m[3][2] * r.m[2][1])
        r.m[3][2] = -(m[3][0] * r.m[0][2] + m[3][1] * r.m[1][2] + m[3][2] * r.m[2][2])

        return r

    #note that this only works when scaling is 1.0
    def get_fast_inverse():
        base = matrix4.Matrix4.from_matrix3x4(self)

        base.m[3][0] = 0.0
        base.m[3][1] = 0.0
        base.m[3][2] = 0.0
        base.m[3][3] = 1.0

        inverse = base.get_transpose()

        x,y,z = self.m[3][0], self.m[3][1], self.m[3][2]

        inverse.m[3][0] = -(inverse.m[0][0] * x + inverse.m[1][0] * y + inverse.m[2][0] * z)
        inverse.m[3][1] = -(inverse.m[0][1] * x + inverse.m[1][1] * y + inverse.m[2][1] * z)
        inverse.m[3][2] = -(inverse.m[0][2] * x + inverse.m[1][2] * y + inverse.m[2][2] * z)

        return Matrix3x4.from_matrix4(inverse)


    @staticmethod
    def interpolate(m1, m2, p):

        inv = (1.0 - p)
        r = Matrix3x4()
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

        r.m[3][0] = a[3][0] * inv + b[3][0] * p
        r.m[3][1] = a[3][1] * inv + b[3][1] * p
        r.m[3][2] = a[3][2] * inv + b[3][2] * p

        return r

    #only tranpose the 3x3 (rotation) part
    def get_transpose(self):
        result = Matrix3x4()

        result.m[0][0] = self.m[0][0]
        result.m[0][1] = self.m[1][0]
        result.m[0][2] = self.m[2][0]


        result.m[1][0] = self.m[0][1]
        result.m[1][1] = self.m[1][1]
        result.m[1][2] = self.m[2][1]

        result.m[2][0] = self.m[0][2]
        result.m[2][1] = self.m[1][2]
        result.m[2][2] = self.m[2][2]

        result.m[3][0] = self.m[3][0]
        result.m[3][1] = self.m[3][1]
        result.m[3][2] = self.m[3][2]

        return result



    def as_single_array(self):
        a = self.m

        return [
            a[0][0],
            a[1][0],
            a[2][0],
            a[3][0],

            a[0][1],
            a[1][1],
            a[2][1],
            a[3][1],

            a[0][2],
            a[1][2],
            a[2][2],
            a[3][2],
        ]




    def __mul__(self, other):
        d = Matrix3x4()
        c = d.m
        a = self.m
        b = other.m

        c[0][0] = a[0][0] * b[0][0] + a[1][0] * b[0][1] + a[2][0] * b[0][2]
        c[1][0] = a[0][0] * b[1][0] + a[1][0] * b[1][1] + a[2][0] * b[1][2]
        c[2][0] = a[0][0] * b[2][0] + a[1][0] * b[2][1] + a[2][0] * b[2][2]
        c[3][0] = a[0][0] * b[3][0] + a[1][0] * b[3][1] + a[2][0] * b[3][2] + a[3][0]

        c[0][1] = a[0][1] * b[0][0] + a[1][1] * b[0][1] + a[2][1] * b[0][2]
        c[1][1] = a[0][1] * b[1][0] + a[1][1] * b[1][1] + a[2][1] * b[1][2]
        c[2][1] = a[0][1] * b[2][0] + a[1][1] * b[2][1] + a[2][1] * b[2][2]
        c[3][1] = a[0][1] * b[3][0] + a[1][1] * b[3][1] + a[2][1] * b[3][2] + a[3][1]

        c[0][2] = a[0][2] * b[0][0] + a[1][2] * b[0][1] + a[2][2] * b[0][2]
        c[1][2] = a[0][2] * b[1][0] + a[1][2] * b[1][1] + a[2][2] * b[1][2]
        c[2][2] = a[0][2] * b[2][0] + a[1][2] * b[2][1] + a[2][2] * b[2][2]
        c[3][2] = a[0][2] * b[3][0] + a[1][2] * b[3][1] + a[2][2] * b[3][2] + a[3][2]

        return d


    def __repr__(self):
        result = ""

        for x in range(0,3):
            for y in range(0,3):
                result = result + "[" + str( round( self.m[y][x], 4) ).ljust(8, '0')[0:8] + "]"

            result = result + "[" + str(round(self.m[3][x], 4 ) ).ljust(8, '0')[0:8] + "]"
            result = result + "\n"

        return result + "\n"
