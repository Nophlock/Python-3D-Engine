
import os
from pyglet import image


class TexturePool:

	def __init__(self):
		self.textures = {}


	def load_texture(self, name, base_path, file_name):

		if name in self.textures:
			print("TexturePool: Warning texture name is already given - ", name)
			return

		file_path = base_path + "/" + file_name
		abs_file_path = os.path.abspath(file_path)

		if os.path.exists(abs_file_path) == False:
			base_name = os.path.basename(os.path.splitext(file_path)[0])
			found_match = False
			possible_files = os.listdir(base_path)

			for file in possible_files:

				if base_name in file:
					file_path = base_path + "/" + file
					abs_file_path = os.path.abspath(file_path)
					found_match = True
					break

			if found_match == False:
				print("TexturePool: Couldnt resolve file_name - ", file_path)
				return

		picture = image.load(abs_file_path )

		self.textures[name] = {}
		self.textures[name]["image"] = picture
		self.textures[name]["texture"] = picture.get_texture()




	def get_texture(self, name):

		if name in self.textures:
			return self.textures[name]

		return None
