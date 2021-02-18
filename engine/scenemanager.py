
from pyglet.gl 		import *
from cube_mesh  	import CubeMeshLoader
from obj_mesh_loader import OBJMeshLoader
from iqm_loader		import IQMLoader
from normal_shader	import NormalShader
from vector3		import Vector3
from matrix4 		import Matrix4
from transform 		import Transform
from quaternion 	import Quaternion
from fpscamera		import FPSCamera
from texture_pool	import TexturePool

import random
import math

class SceneManager:

	def __init__(self, engine):
		self.engine			= engine

		self.time = 0
		self.camera 		= FPSCamera(engine)
		self.texture_pool	= TexturePool()
		self.objects		= []

		self.camera.set_perspective_matrix(70.0, 800.0/600.0, 0.001, 10000.0)
		self.create_test_scene()

		glDepthFunc(GL_LESS)
		glCullFace(GL_FRONT)
		glClearColor(0.5, 0.5, 0.5, 0.0);


	def create_test_scene(self):

		self.loader = OBJMeshLoader(self)#IQMLoader(self)
		#self.loader = IQMLoader(self)

		self.tests = self.loader.get_mesh("data/models/objs/multiple_meshes.obj")#self.loader.get_mesh("data/models/iqms/mrfixit/mrfixit.iqm")
		#self.tests = self.loader.get_mesh("data/models/iqms/mrfixit/mrfixit.iqm")
		self.shader	= NormalShader()

		self.transform = Transform()

		#for testing we say the mesh is at the origin for now
		quat = Quaternion( Vector3(0.0, 0.0, -1.0), 3.141 * 0.5).get_axis_quaternion()
		quat = quat * Quaternion( Vector3(0.0, -1.0, 0.0), 3.141 * 0.5).get_axis_quaternion()

		self.transform.set_local_position ( Vector3(0.0,-5.0,-10.0))
		self.transform.set_local_rotation (quat.get_normalized() )


		if self.tests[0].has_animations():
			anim_names = self.tests[0].get_animation_player().get_animation_names()


			for i in range(len(self.tests)):
				self.tests[i].get_animation_player().play_animation("idle", 1.0)


	def update_scene(self, dt):
		self.camera.update(dt)

		for i in range(len(self.tests)):

			if self.tests[i].is_animation_root():
				self.tests[i].get_animation_player().update(dt)


		self.time = self.time + dt


	def resize_viewport(self, width, height):
		glViewport(0, 0, width, height)
		self.camera.set_perspective_matrix(70.0, width/height, 0.001, 10000.0)

	def get_texture_pool(self):
		return self.texture_pool


	def render(self):
		self.prepare_render_scene()
		self.render_scene(self.camera, self.shader)

	def render_scene(self, camera, shader):

		shader.bind()

		shader.send_float (shader.get_location("time") , abs( math.sin( 0.0 ) / 2.0 ) + 0.5 )
		shader.send_matrix_4 (shader.get_location("perspective_matrix") , self.camera.get_perspective_matrix() )
		shader.send_matrix_4 (shader.get_location("camera_matrix") , self.camera.get_transformation_matrix() )

		shader.send_matrix_4 (shader.get_location("transformation_matrix") , self.transform.get_transformation_matrix())


		for i in range(len(self.tests)):
			shader.prepare_render(self.tests[i])
			self.tests[i].render(self)


		shader.unbind()



	def prepare_render_scene(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		glEnable(GL_DEPTH_TEST)
		#glEnable(GL_CULL_FACE)

	def set_active_camera(self, new_camera):
		self.camera = new_camera

	def get_active_camera(self):
		return self.camera
