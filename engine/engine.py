
from pyglet.gl 		import *
from keymapper		import KeyMapper
from scenemanager	import SceneManager

import os
import math
import time


class Engine(pyglet.window.Window):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.set_minimum_size(50, 50)

		self.init()
		pyglet.clock.schedule( self.update )

		self.set_vsync(False)

		self.frame_tick = 0.0
		self.frames = 0
		self.physic_engine_fps = 100
		self.physic_engine_delta = 1.0 / self.physic_engine_fps

		self.accumulator = 0.0
		self.frame_start = time.time()


	def init(self):
		self.key_mapper		= KeyMapper()
		self.scene_manager	= SceneManager(self)





	def on_draw(self):
		self.clear()
		self.scene_manager.render()



	def update(self, dt):

		current_time = time.time()
		self.accumulator = self.accumulator + current_time - self.frame_start
		self.frame_start = current_time

		#avoid infinity loop if the updates goes to slow
		if self.accumulator > 0.2:
			self.accumulator = 0.2


		while(self.accumulator > dt):
			self.scene_manager.fixed_update(self.physic_engine_delta)
			self.accumulator = self.accumulator - self.physic_engine_delta



		#this stuff here should run seperatly from our physics engine
		self.key_mapper.update()
		self.scene_manager.update(dt)

		self.frames = self.frames + 1
		self.frame_tick = self.frame_tick + dt

		if self.frame_tick >= 1.0:
			print("FPS: ", self.frames)

			self.frame_tick = 0.0
			self.frames = 0



		#if dt > 0.0:
			#os.system('cls')
			#print(math.floor(1.0 / dt) )

	def exit(self):
		self.close()

	def on_resize(self, width, height):
		self.scene_manager.resize_viewport(width, height)

	def on_key_press(self, key, modifier):
		#print(modifier)
		#fixme add modifier as keytype
		self.key_mapper.update_key_pressed(str(key) )

	def on_key_release(self, key, modifier):
		self.key_mapper.update_key_released(str(key) )

	def on_mouse_press(self, x,y, button, modifier):
		self.key_mapper.update_key_pressed("m_" + str(button) )

	def on_mouse_release(self, x,y, button, modifier):
		self.set_mouse_visible(True)
		self.key_mapper.update_key_released("m_" + str(button) )

	def on_mouse_drag(self, x, y, dx, dy, button, modifier):
		self.key_mapper.update_mouse_input(x,y, dx, dy)

	def on_mouse_motion(self, x, y, dx, dy):
		self.key_mapper.update_mouse_input(x,y, dx, dy)


	def get_key_mapper(self):
		return self.key_mapper

	def get_scene_manager(self):
		return self.scene_manager



def main():
	#freeze_support()
	engine = Engine(width=800, height=600, caption="Python 3D-Engine", resizable=True)
	pyglet.app.run()
	engine.exit()

	import sys
	sys.exit()

if __name__ ==  '__main__':
	main()
