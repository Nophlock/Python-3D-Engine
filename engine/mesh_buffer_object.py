
from pyglet.gl 	import *
import ctypes


class MeshBufferObject:

	def __init__(self):

		self.type = GL_TRIANGLES
		self.is_build = False

		self.length = 0
		self.data_type = GL_UNSIGNED_INT
		self.attrib_count = 0
		self.vao_index = 0

		self.attributes	= {}
		self.buffer_index = {}


	def clear_buffer(self):

		if self.is_build:
			glDeleteVertexArrays(1, self.vao_index)

			for entry in self.buffer_index:
				glDeleteBuffers(1,self.buffer_index[entry]["index"])

			self.__init__()



	def prepare_buffer(self, _type, length, type, attribts):

		self.type = _type
		self.length = length
		self.data_type = type
		self.attributes = attribts


	def __del__(self):

		if(self.is_build == True):
			pass#glDeleteBuffers		(1, ctypes.pointer(self.vbo_index) )
			#glDeleteVertexArrays(1, ctypes.pointer(self.vao_index) )

	def create_buffer(self):

		self.vao_index = GLuint(0)
		glGenVertexArrays(1, self.vao_index)
		glBindVertexArray(self.vao_index)


		for entry in self.attributes:
			self.buffer_index[entry] = {}
			self.buffer_index[entry]["index"] = GLuint(0)
			self.buffer_index[entry]["type"] = self.attributes[entry]["type"]

			glGenBuffers(1, self.buffer_index[entry]["index"])

			glBindBuffer(self.buffer_index[entry]["type"], self.buffer_index[entry]["index"])
			glBufferData(self.buffer_index[entry]["type"], self.attributes[entry]["size"], self.attributes[entry]["data"], GL_STATIC_DRAW)

			if "attributes" in self.attributes[entry]:
				for i in range(len(self.attributes[entry]["attributes"]) ):

					glVertexAttribPointer(self.attrib_count, self.attributes[entry]["attributes"][i]["size"], self.attributes[entry]["attributes"][i]["type"], self.attributes[entry]["attributes"][i]["normalized"],
										  self.attributes[entry]["attributes"][i]["stride"], self.attributes[entry]["attributes"][i]["offset"])
					glEnableVertexAttribArray(self.attrib_count)
					glDisableVertexAttribArray(self.attrib_count)

					self.attrib_count = self.attrib_count + 1

			#unbinding
			glBindBuffer(self.buffer_index[entry]["type"], 0)


		#unbinding
		glBindVertexArray(0)
		self.is_build = True


	def get_type_count(self):
		if self.type == GL_TRIANGLES:
			return 3
		else:
			return 4


	def render(self):

		if self.is_build == False:
			return

		glBindVertexArray(self.vao_index)

		#activate attributes
		for i in range(self.attrib_count):
			glEnableVertexAttribArray(i)


		for entry in self.buffer_index:
			glBindBuffer(self.buffer_index[entry]["type"],self.buffer_index[entry]["index"])

		glDrawElements(self.type, self.length, self.data_type, 0 )


		#deactivate attributes
		for i in range(self.attrib_count):
			glDisableVertexAttribArray(i)

		for entry in self.buffer_index:
			glBindBuffer(self.buffer_index[entry]["type"],0)

		glBindVertexArray(0)
