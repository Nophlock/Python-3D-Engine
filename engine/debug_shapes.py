
import ctypes
from pyglet.gl 	import *

from mesh import Mesh
from engine_math import vector3

import math

class DebugShapes:


    @staticmethod
    def create_aabb_shape(aabb):

        knots = aabb.get_transformed_knots()
        vertices = []
        ibo = [0,1,3,2,0, 4,5,1,0,4, 6,7,5,7, 3,2,6]

        for i in range(8):
            vertices.append(knots[i].x)
            vertices.append(knots[i].y)
            vertices.append(knots[i].z)

        data = {}

        data["vbo"] = {}
        data["vbo"]["type"] = GL_ARRAY_BUFFER
        data["vbo"]["size"] = ctypes.sizeof(GLfloat * len(vertices))
        data["vbo"]["data"] = (GLfloat * len(vertices)) (*vertices)
        data["vbo"]["attributes"] = [{}]

        data["vbo"]["attributes"][0]["size"] = 3
        data["vbo"]["attributes"][0]["type"] = GL_FLOAT
        data["vbo"]["attributes"][0]["stride"] = 0
        data["vbo"]["attributes"][0]["offset"] = 0
        data["vbo"]["attributes"][0]["normalized"] = GL_FALSE


        data["ibo"] = {}
        data["ibo"]["type"] = GL_ELEMENT_ARRAY_BUFFER
        data["ibo"]["size"] = ctypes.sizeof(GLuint * len(ibo))
        data["ibo"]["data"] = (GLuint * len(ibo)) (*ibo)

        mesh = Mesh("dbg_aabb")

        mesh.get_buffer().clear_buffer()
        mesh.get_buffer().prepare_buffer(GL_LINE_STRIP, len(ibo),GL_UNSIGNED_INT, data)
        mesh.get_buffer().create_buffer()

        return mesh

    @staticmethod
    def create_box_shape(w, h, d):

        points = []
        vertices = []
        ibo = [0,1,3,2,0, 4,5,1,0,4, 6,7,5,7, 3,2,6]

        h_w = w * 0.5
        h_h = h * 0.5
        h_d = d * 0.5

        points.append(vector3.Vector3(-h_w, -h_h, -h_d)) #000
        points.append(vector3.Vector3(-h_w, -h_h, h_d)) #001
        points.append(vector3.Vector3(-h_w, h_h, -h_d)) #010
        points.append(vector3.Vector3(-h_w, h_h, h_d)) #011
        points.append(vector3.Vector3(h_w, -h_h, -h_d)) #100
        points.append(vector3.Vector3(h_w, -h_h, h_d)) #101
        points.append(vector3.Vector3(h_w, h_h, -h_d)) #110
        points.append(vector3.Vector3(h_w, h_h, h_d)) #111

        for i in range(8):
            vertices.append(points[i].x)
            vertices.append(points[i].y)
            vertices.append(points[i].z)

        data = {}

        data["vbo"] = {}
        data["vbo"]["type"] = GL_ARRAY_BUFFER
        data["vbo"]["size"] = ctypes.sizeof(GLfloat * len(vertices))
        data["vbo"]["data"] = (GLfloat * len(vertices)) (*vertices)
        data["vbo"]["attributes"] = [{}]

        data["vbo"]["attributes"][0]["size"] = 3
        data["vbo"]["attributes"][0]["type"] = GL_FLOAT
        data["vbo"]["attributes"][0]["stride"] = 0
        data["vbo"]["attributes"][0]["offset"] = 0
        data["vbo"]["attributes"][0]["normalized"] = GL_FALSE


        data["ibo"] = {}
        data["ibo"]["type"] = GL_ELEMENT_ARRAY_BUFFER
        data["ibo"]["size"] = ctypes.sizeof(GLuint * len(ibo))
        data["ibo"]["data"] = (GLuint * len(ibo)) (*ibo)

        mesh = Mesh("dbg_aabb")

        mesh.get_buffer().clear_buffer()
        mesh.get_buffer().prepare_buffer(GL_LINE_STRIP, len(ibo),GL_UNSIGNED_INT, data)
        mesh.get_buffer().create_buffer()

        return mesh

    @staticmethod
    def create_tetrahedron_shape(simplex, ibo):

        vertices = []

        for i in range(len(simplex)):
            vertices.append( simplex[i][0].x )
            vertices.append( simplex[i][0].y )
            vertices.append( simplex[i][0].z )

        data = {}

        data["vbo"] = {}
        data["vbo"]["type"] = GL_ARRAY_BUFFER
        data["vbo"]["size"] = ctypes.sizeof(GLfloat * len(vertices))
        data["vbo"]["data"] = (GLfloat * len(vertices)) (*vertices)
        data["vbo"]["attributes"] = [{}]

        data["vbo"]["attributes"][0]["size"] = 3
        data["vbo"]["attributes"][0]["type"] = GL_FLOAT
        data["vbo"]["attributes"][0]["stride"] = 0
        data["vbo"]["attributes"][0]["offset"] = 0
        data["vbo"]["attributes"][0]["normalized"] = GL_FALSE


        data["ibo"] = {}
        data["ibo"]["type"] = GL_ELEMENT_ARRAY_BUFFER
        data["ibo"]["size"] = ctypes.sizeof(GLuint * len(ibo))
        data["ibo"]["data"] = (GLuint * len(ibo)) (*ibo)

        mesh = Mesh("dbg_tetrahedron")

        mesh.get_buffer().clear_buffer()
        mesh.get_buffer().prepare_buffer(GL_TRIANGLES, len(ibo),GL_UNSIGNED_INT, data)
        mesh.get_buffer().create_buffer()

        return mesh

    #based on https://www.songho.ca/opengl/gl_sphere.html
    @staticmethod
    def create_point_shape(point,radius, rings, sectors):
        vertices = []
        ibo = []

        R = 1.0 / (rings-1)
        S = 1.0 / (sectors-1)

        pi_2 = math.pi / 2.0
        pi = math.pi


        for r in range(rings):
            for s in range(sectors):

                y = math.sin(-pi_2 + (pi * r * R) )
                x = math.cos(2.0*pi * s * S) * math.sin(pi * r * R)
                z = math.sin(2.0*pi * s * S) * math.sin(pi * r * R)

                vertices.append(point.x + x * radius)
                vertices.append(point.y + y * radius)
                vertices.append(point.z + z * radius)


        for r in range(rings):
            for s in range(sectors):
                ibo.append(r * sectors + s)
                ibo.append(r * sectors + (s+1))
                ibo.append((r+1) * sectors + (s+1) )
                ibo.append((r+1) * sectors + s)


        data = {}

        data["vbo"] = {}
        data["vbo"]["type"] = GL_ARRAY_BUFFER
        data["vbo"]["size"] = ctypes.sizeof(GLfloat * len(vertices))
        data["vbo"]["data"] = (GLfloat * len(vertices)) (*vertices)
        data["vbo"]["attributes"] = [{}]

        data["vbo"]["attributes"][0]["size"] = 3
        data["vbo"]["attributes"][0]["type"] = GL_FLOAT
        data["vbo"]["attributes"][0]["stride"] = 0
        data["vbo"]["attributes"][0]["offset"] = 0
        data["vbo"]["attributes"][0]["normalized"] = GL_FALSE


        data["ibo"] = {}
        data["ibo"]["type"] = GL_ELEMENT_ARRAY_BUFFER
        data["ibo"]["size"] = ctypes.sizeof(GLuint * len(ibo))
        data["ibo"]["data"] = (GLuint * len(ibo)) (*ibo)

        mesh = Mesh("dbg_point_sphere")

        mesh.get_buffer().clear_buffer()
        mesh.get_buffer().prepare_buffer(GL_QUADS, len(ibo),GL_UNSIGNED_INT, data)
        mesh.get_buffer().create_buffer()

        return mesh
