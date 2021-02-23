
from ctypes 	import *
from pyglet.gl 	import *

class Shader:
	def __init__(self):
		self.program = glCreateProgram()

	def get_file_content(self, filename):
		return open(filename).read()

	def log_error(self, object, state):
		length = c_int(0)
		glGetProgramInfoLog(object, GL_OBJECT_INFO_LOG_LENGTH_ARB, byref(length))
		log = create_string_buffer(length.value)

		print('failed to ' + state + ' shader:\n%s' % log.value)

	def add_shader(self, type, shader_file):
		shader = glCreateShader(type)
		content	= self.get_file_content(shader_file)
		ptr_content = cast(c_char_p(content.encode('utf-8')), POINTER(c_char))

		glShaderSourceARB(shader, 1, byref(ptr_content), None)
		glCompileShader(shader)

		status = c_int(0)
		glGetObjectParameterivARB(shader, GL_OBJECT_COMPILE_STATUS_ARB, byref(status))

		if status.value == 0:

			length = c_int(0)
			glGetObjectParameterivARB(shader, GL_OBJECT_INFO_LOG_LENGTH_ARB, byref(length))
			log = create_string_buffer(length.value)
			glGetInfoLogARB(shader, length.value, None, log)

			print('failed to compile:\n%s' % log.value)
			return False
		else:
			glAttachShader(self.program, shader);
			return True

	def compile_shader(self):

		glLinkProgram(self.program);

		status = c_int(0)
		glGetProgramiv(self.program, GL_LINK_STATUS, byref(status))

		if status.value == 0:
			self.log_error(self.program, 'link')
			return False


		glValidateProgram(self.program)
		glGetObjectParameterivARB(self.program, GL_VALIDATE_STATUS, byref(status))

		if status.value == 0:
			self.log_error(self.program, 'validate')
			return False

		return True

	def get_uniform_location(self, name):
		return glGetUniformLocation(self.program, name.encode())

	def send_float(self, location, value):
		glUniform1f(location, value)

	def send_integer(self, location, value):
		glUniform1i(location, value)

	def send_matrix_4(self, location, matrix):
		glUniformMatrix4fv(location, 1, GL_FALSE, (GLfloat * 16 )(*matrix.as_single_array() ) )

	def send_vector4(self, location, array):
		glUniform4f(location,  array[0], array[1], array[2], array[3] )

	def send_matrix4_array(self, location, matrix_array):

		arr = []
		count = len(matrix_array)
		c_type = GLfloat * (count * 16)

		for i in range(count):
			arr.extend( matrix_array[i].as_single_array() )

		data = c_type (*arr)
		data_ptr = cast(data, POINTER(c_float))

		glUniformMatrix4fv(location, count, GL_FALSE, data_ptr)


	#https://github.com/gabdube/pyshaders/blob/master/pyshaders.py for reference
	def send_matrix3x4_array(self, location, matrix_array):

		arr = []
		count = len(matrix_array)
		c_type = GLfloat * (count * 12)

		for i in range(count):
			arr.extend( matrix_array[i].as_single_array() )

		data = c_type (*arr)
		data_ptr = cast(data, POINTER(c_float))

		glUniformMatrix3x4fv(location, count, GL_FALSE, data_ptr)


	def bind(self):
		glUseProgram(self.program)

	def unbind(self):
		glUseProgram(0)
