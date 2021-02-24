
from pyglet.gl 		import *
from cube_mesh  	import CubeMeshLoader
from normal_shader	import NormalShader
from transform 		import Transform
from fpscamera		import FPSCamera
from texture_pool	import TexturePool
from debug_mesh		import DebugMesh
from mesh_loaders	import mesh_loader
from material		import Material
from physics		import gjk
from physics		import epa


from engine_math	import vector3
from engine_math 	import matrix4
from engine_math	import quaternion

import random
import math

class SceneManager:

	def __init__(self, engine):
		self.engine	= engine

		self.time = 0
		self.camera 		= FPSCamera(engine)
		self.texture_pool	= TexturePool()

		self.objects		= []
		self.debug_shapes	= []

		self.camera.set_perspective_matrix(70.0, 800.0/600.0, 0.001, 10000.0)
		self.create_test_scene()

		glDepthFunc(GL_LESS)
		glCullFace(GL_FRONT)
		glClearColor(0.5, 0.5, 0.5, 0.0);


	def create_test_scene(self):
		self.loader = mesh_loader.MeshLoader(self)

		self.objects.extend( self.loader.get_meshs("data/models/objs/monkey.obj") )
		self.objects.extend( self.loader.get_meshs("data/models/objs/monkey.obj") )
		#self.objects.extend( self.loader.get_meshs("data/models/iqms/mrfixit/mrfixit.iqm") )
		self.debug_shapes.append(DebugMesh(self, self.objects[0]) )
		self.debug_shapes.append(DebugMesh(self, self.objects[1]) )

		tot_triangles = 0
		tot_vertices = 0
		tot_bones = 0

		for i in range(len(self.objects)):
			info = self.objects[i].get_informations()

			if info == None:
				continue

			tot_triangles = tot_triangles + info["num_triangles"]
			tot_vertices = tot_vertices + info["num_vertices"]

			if self.objects[i].is_animation_root():
				tot_bones = tot_bones + info["num_bones"]

		print("[Scene stats]")
		print("Total triangles: ", tot_triangles)
		print("Total vertices: ", tot_vertices)
		print("Total bones: ", tot_bones)


		self.tmp_aabb = self.objects[1].get_aabb()
		self.shader	= NormalShader(self)

		self.transform = Transform()
		self.transform2 = Transform()

		#for testing we say the mesh is at the origin for now
		quat = quaternion.Quaternion( vector3.Vector3(0.0, 0.0, -1.0), 3.141 * 0.5).get_axis_quaternion()
		quat = quat * quaternion.Quaternion( vector3.Vector3(0.0, -1.0, 0.0), 3.141 * 0.5).get_axis_quaternion()

		self.t1_position = vector3.Vector3(0.0,-5.0,-10.0)

		self.transform.set_local_position ( self.t1_position)
		self.transform.set_local_rotation (quat.get_normalized() )

		self.transform2.set_local_position ( vector3.Vector3(5.0,-5.0,-10.0))
		self.transform2.set_local_rotation ( quat.get_normalized() )

		for i in range(len(self.objects)):

			if self.objects[i].has_animations():
				anim_names = self.objects[i].get_animation_player().get_animation_names()
				self.objects[i].get_animation_player().play_animation("idle", 1.0)



	def update_scene(self, dt):
		self.camera.update(dt)

		quat = self.transform.get_local_rotation() * quaternion.Quaternion(vector3.Vector3(0.0, 1.0, -1.0), 0.05*dt).get_axis_quaternion()
		self.transform.set_local_rotation ( quaternion.Quaternion.from_axis(vector3.Vector3(), 1.0) )

		self.transform.set_local_position(self.t1_position + vector3.Vector3(math.sin(self.time) * 5.0, 1.0, 0.0) )

		for i in range(len(self.objects)):

			if self.objects[i].is_animation_root():
				self.objects[i].get_animation_player().update(dt)

		for i in range(len(self.debug_shapes)):

			if i == 0: self.debug_shapes[i].update(self.transform, dt)
			else: self.debug_shapes[i].update(self.transform2, dt)

		poly_a = self.objects[0].get_aabb().get_transformed_knots()
		poly_b = self.objects[1].get_aabb().get_transformed_knots()

		col, simplex = gjk.GJK.is_polygon_colliding(poly_a, poly_b)

		if col:
			min_normal, min_distance = epa.EPA.get_penetration_data(simplex, poly_a, poly_b)

			self.transform.set_local_position(self.transform.get_local_position() + min_normal * -min_distance)

			self.objects[0].get_default_material().assign_material("mesh_color", [1.0, 0.0, 0.0, 1.0])
		else:
			self.objects[0].get_default_material().assign_material("mesh_color", [1.0, 1.0, 1.0, 1.0])

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



		for i in range(len(self.objects)):

			if i == 0:
				shader.send_matrix_4 (shader.get_location("transformation_matrix") , self.transform.get_transformation_matrix())
			else:
				shader.send_matrix_4 (shader.get_location("transformation_matrix") , self.transform2.get_transformation_matrix())

			mat = self.objects[i].get_default_material()

			shader.prepare_render(self.objects[i], mat)
			self.objects[i].render()
			shader.unprepare_render(self.objects[i], mat)


		shader.send_matrix_4 (shader.get_location("transformation_matrix") , matrix4.Matrix4())

		for i in range(len(self.debug_shapes)):
			mat = self.debug_shapes[i].get_default_material()

			shader.prepare_render(self.debug_shapes[i], mat)
			self.debug_shapes[i].render()
			shader.unprepare_render(self.debug_shapes[i], mat)


		shader.unbind()



	def prepare_render_scene(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		glEnable(GL_DEPTH_TEST)
		#glEnable(GL_CULL_FACE)

	def set_active_camera(self, new_camera):
		self.camera = new_camera

	def get_active_camera(self):
		return self.camera
