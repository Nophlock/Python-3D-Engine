
import ctypes
from pyglet.gl 	import *

from mesh import Mesh
from engine_math import vector3

class DebugShapes:


    @staticmethod
    def create_aabb_shape(mesh, aabb):

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

        mesh.get_buffer().clear_buffer()
        mesh.get_buffer().prepare_buffer(GL_LINE_STRIP, len(ibo),GL_UNSIGNED_INT, data)
        mesh.get_buffer().create_buffer()
