

class KeyMapper:

	def __init__(self):
		self.key_constants = {}

		self.mouse_flush = False
		self.mx = 0.0
		self.my = 0.0
		self.dx = 0.0
		self.dy = 0.0


	def update_mouse_input(self, x, y, dx, dy):
		self.mx = x
		self.my = y
		self.dx = dx
		self.dy = dy

		self.mouse_flush = False


	def get_mouse_position(self):
		return (self.mx,self.my)

	def get_mouse_relative_position(self):
		return (self.dx, self.dy)

	def update_key_pressed(self, key):
		as_string = str(key)

		if(not as_string in self.key_constants):
			self.key_constants[as_string] = {"is_pressed": False, "is_released": False, "is_holded": False}

		self.key_constants[as_string]["is_pressed"] = True

	def update_key_released(self, key):
		as_string = str(key)

		self.key_constants[as_string]["is_pressed"] = False
		self.key_constants[as_string]["is_holded"]	= False
		self.key_constants[as_string]["is_released"]= True

	def update(self):


		if self.mouse_flush:
			self.dx = 0
			self.dy = 0

		self.mouse_flush = True

		for key in self.key_constants:

			if self.key_constants[key]["is_pressed"] == True:
				self.key_constants[key]["is_pressed"] = False
				self.key_constants[key]["is_holded"] = True
			elif self.key_constants[key]["is_released"] == True:
				self.key_constants[key]["is_released"] = False


	def is_key_pressed(self, name):
		as_string = str(name)

		if(not as_string in self.key_constants):
			return False

		return self.key_constants[as_string]["is_pressed"]

	def is_key_holded(self, name):
		as_string = str(name)

		if(not as_string in self.key_constants):
			return False


		return self.key_constants[as_string]["is_holded"]

	def is_key_released(self, name):
		as_string = str(name)

		if(not as_string in self.key_constants):
			return False

		return self.key_constants[as_string]["is_released"]
