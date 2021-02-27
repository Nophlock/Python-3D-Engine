
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

from entity import Entity
from components import mesh_renderer
from components import mesh_debug_renderer


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
		self.shader = NormalShader(self)

		self.entities = []
		self.stop = False

		self.camera.set_perspective_matrix(70.0, 800.0/600.0, 0.001, 10000.0)
		self.create_test_scene()

		glDepthFunc(GL_LESS)
		glCullFace(GL_FRONT)
		glClearColor(0.5, 0.5, 0.5, 0.0);


	def create_test_scene(self):
		self.loader = mesh_loader.MeshLoader(self)
		self.mesh_pool = []
		self.mesh_pool.append(self.loader.get_meshs("data/models/objs/cube.obj"))
		self.mesh_pool.append(self.loader.get_meshs("data/models/objs/ground_box.obj"))
		#self.mesh_pool.append(self.loader.get_meshs("data/models/iqms/mrfixit/mrfixit.iqm"))

		ent = Entity()
		ent.add_component(mesh_renderer.MeshRenderer(self.mesh_pool[0]) )
		ent.add_component(mesh_debug_renderer.MeshDebugRenderer())

		self.entities.append(ent)

		ent2 = Entity()
		ent2.add_component(mesh_renderer.MeshRenderer(self.mesh_pool[0]) )
		ent2.add_component(mesh_debug_renderer.MeshDebugRenderer())

		self.entities.append(ent2)

		ent3 = Entity()
		ent3.add_component(mesh_renderer.MeshRenderer(self.mesh_pool[1]) )
		ent3.add_component(mesh_debug_renderer.MeshDebugRenderer())

		self.entities.append(ent3)


		#for testing we say the mesh is at the origin for now
		quat = quaternion.Quaternion( vector3.Vector3(0.0, 0.0, -1.0), 3.141 * 0.5).get_axis_quaternion()
		quat = quat * quaternion.Quaternion( vector3.Vector3(0.0, -1.0, 0.0), 3.141 * 0.5).get_axis_quaternion()

		self.t1_position = vector3.Vector3(0.0,-5.0,-10.0)

		self.entities[0].get_transform().set_local_rotation( quaternion.Quaternion.from_axis(vector3.Vector3(), 1.0) )
		self.entities[0].get_transform().set_local_position( self.t1_position )

		self.entities[1].get_transform().set_local_rotation(  quat.get_normalized() )
		self.entities[1].get_transform().set_local_position( vector3.Vector3(5.0,-5.0,-10.0) )

		self.entities[0].get_component("MeshRenderer").play_animation("idle", 1.0)
		self.entities[1].get_component("MeshRenderer").play_animation("idle", 1.0)

		self.entities[2].get_transform().set_local_position( vector3.Vector3(0.0, -8, 0.0) )
		self.entities[2].get_component("MeshRenderer").get_materials()[0].assign_material("mesh_color", [0.5, 0.5, 0.5, 1.0])


		#for i in range(len(self.objects)):

		#	if self.objects[i].has_animations():
		#		anim_names = self.objects[i].get_animation_player().get_animation_names()
		#		self.objects[i].get_animation_player().play_animation("idle", 1.0)

	def fixed_update(self, dt):

		for i in range(len(self.entities)):
			self.entities[i].fixed_update(dt)


	def custom_test_update(self, dt):

		if self.stop == False:
			self.entities[0].get_transform().set_local_position( self.t1_position + vector3.Vector3(math.sin(self.time) * 5.0, 1.0, 0.0) )
			self.time = self.time + dt

		m_render_1 = self.entities[0].get_component("MeshRenderer")
		m_render_2 = self.entities[1].get_component("MeshRenderer")

		#this is a hacky solution to avoid jittering, which is caused by the matrix not recalculating in this frame and therefore not updating the aabb (so our knots point at
		# a position where the meshes didnt collide, which cause flickering)
		# this will works for now until i come up with something better than this (if this is even required since this is only for testing here)
		self.entities[0].get_transform().get_transformation_matrix()

		col = m_render_1.get_aabb().is_aabb_inside_aabb(m_render_2.get_aabb())

		if col:

			poly_a = m_render_1.get_aabb().get_transformed_knots()
			poly_b = m_render_2.get_aabb().get_transformed_knots()

			col, simplex = gjk.GJK.is_polygon_colliding(poly_a, poly_b)


		if col:
			min_normal, min_distance = epa.EPA.get_penetration_data(simplex, poly_a, poly_b)

			self.entities[0].get_transform().set_local_position(self.entities[0].get_transform().get_local_position() + min_normal * -min_distance)
			m_render_1.get_materials()[0].assign_material("mesh_color", [1.0, 0.0, 0.0, 1.0])

		else:
			m_render_1.get_materials()[0].assign_material("mesh_color", [1.0, 1.0, 1.0, 1.0])



	def update(self, dt):
		self.camera.update(dt)


		for i in range(len(self.entities)):
			self.entities[i].update(dt)

		self.custom_test_update(dt)


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

		for i in range(len(self.entities)):
			self.entities[i].render(camera, shader)

		shader.unbind()



	def prepare_render_scene(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		glEnable(GL_DEPTH_TEST)
		#glEnable(GL_CULL_FACE)

	def set_active_camera(self, new_camera):
		self.camera = new_camera

	def get_active_camera(self):
		return self.camera
