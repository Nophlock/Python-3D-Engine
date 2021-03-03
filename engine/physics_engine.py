
from physics		import gjk
from physics		import epa

from components import primitive_render

from entity import Entity
from debug_shapes import DebugShapes

from engine_math import vector3

class PhysicsEngine:

	def __init__(self, scene_mgr):
		self.scene_mgr = scene_mgr
		self.physics_entities = []
		self.collided_entities = []

		self.gravity = vector3.Vector3(0.0, -9.81, 0.0)

		self.debug_contact = 0.0
		self.stop = False


	def add_physics_object(self, entity, resolver):
		self.physics_entities.append([entity, resolver])


	def get_gravity(self):
		return self.gravity


	def fixed_update(self, dt):

		self.debug_contact = self.debug_contact - dt

		if self.stop == True:
			return

		for i in range( len(self.physics_entities) ):

			comp = self.physics_entities[i][1]
			aabb = comp.get_collision_aabb()

			for j in range( len(self.physics_entities) ):

				if i == j:
					continue

				o_comp = self.physics_entities[j][1]
				o_aabb = o_comp.get_collision_aabb()
				collision = aabb.is_aabb_inside_aabb(o_aabb)

				if collision:

					poly_a = self.physics_entities[i][1].get_collision_polygon()
					poly_b = self.physics_entities[j][1].get_collision_polygon()

					collision, simplex = gjk.GJK.is_polygon_colliding(poly_a, poly_b)

					if collision:

						pack = [ self.physics_entities[i], self.physics_entities[j] ]

						if pack not in self.collided_entities:
							self.physics_entities[i][1].collision_started(self.physics_entities[j])
							self.physics_entities[j][1].collision_started(self.physics_entities[i])

							self.collided_entities.append([ self.physics_entities[i], self.physics_entities[j] ])

						col_points, min_normal, min_distance, faces = epa.EPA.get_penetration_data(simplex, poly_a, poly_b)


						#if self.debug_contact < 0.0:


						#	for z in range(len(col_points)):
						#		ent = Entity(self)
						#		ent.add_component(primitive_render.PrimitiveRender(DebugShapes.create_point_shape(col_points[z], 0.25, 8, 8 ) ) )
						#		self.scene_mgr.entities.append(ent)

						#	self.debug_contact = 2.0


						self.physics_entities[i][1].eval_collision(self.physics_entities[j], col_points, min_normal, min_distance)


				if collision == False:
					pack = [ self.physics_entities[i], self.physics_entities[j] ]

					if pack in self.collided_entities:
						pack[0][1].collision_stopped(pack[1])
						pack[1][1].collision_stopped(pack[1])
						self.collided_entities.remove(pack)
