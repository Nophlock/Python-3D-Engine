
from physics		import gjk
from physics		import epa

from material import Material

from components import primitive_render

from entity import Entity
from debug_shapes import DebugShapes

from engine_math import vector3

class PhysicsEngine:

	def __init__(self, scene_mgr):
		self.scene_mgr = scene_mgr
		self.physics_entities = []

		self.gravity = vector3.Vector3(0.0, -9.81, 0.0)

		self.debug_contact = 0.0


	def add_physics_object(self, entity, resolver):
		self.physics_entities.append([entity, resolver, False])


	def get_gravity(self):
		return self.gravity


	def fixed_update(self, dt):

		self.debug_contact = self.debug_contact - dt

		#apply some gravity so we have something to see(only on the rigid body which is the first element)
		for i in range(len(self.physics_entities)):

			if self.physics_entities[i][1].get_name() == "RigidBody":

				#if self.physics_entities[i][1].linear_velocity.get_len() < 0.1 and self.physics_entities[i][1].angular_velocity.get_len() < 0.5:
				#	self.physics_entities[i][1].set_awake(False)

				#	self.physics_entities[i][1].linear_velocity = vector3.Vector3()
				#	self.physics_entities[i][1].angular_velocity = vector3.Vector3()

				#else:
				#	self.physics_entities[i][1].set_awake(True)

				self.physics_entities[i][1].apply_central_force(self.get_gravity())




		self.perform_collision_check(dt)


	def perform_collision_check(self, dt):

		collisions = []

		#first iteration, track all collisions and store them in a table
		for i in range( len(self.physics_entities) ):

			ent = self.physics_entities[i]
			comp = ent[1]
			aabb = comp.get_collision_aabb()

			if comp.get_name() != "RigidBody":
				continue

			collision_data = []

			for j in range( len(self.physics_entities) ):

				if i == j:
					continue

				o_comp = self.physics_entities[j][1]
				o_aabb = o_comp.get_collision_aabb()
				intersect = aabb.is_aabb_inside_aabb(o_aabb)

				if intersect:

					poly_a = self.physics_entities[i][1].get_collision_polygon()
					poly_b = self.physics_entities[j][1].get_collision_polygon()

					intersect, simplex = gjk.GJK.is_polygon_colliding(poly_a, poly_b)

					if intersect:

						mat_a = self.physics_entities[i][0].get_transform().get_transformation_matrix()
						mat_b = self.physics_entities[j][0].get_transform().get_transformation_matrix()

						penetration_data = epa.EPA.get_penetration_data(simplex, poly_a,mat_a, poly_b, mat_b)
						collision_data.append([i,j, penetration_data])


				if len(collision_data) != 0:
					collisions.append(collision_data)
				else:

					if ent[2] == True:
						comp.collision_stopped()
						ent[2] = False


		#in the second step we integrate all our forces
		for i in range(len(self.physics_entities)):

			if self.physics_entities[i][1].get_name() == "RigidBody":
				self.physics_entities[i][1].integrate(dt)

		#in the thrid step we resolve our collisions and update our forces accordingly
		for i in range(len(collisions)):
			col = collisions[i]
			ent = self.physics_entities[col[0][0]]
			col_count = len(col)
			force_distribution = 1.0 / col_count

			if ent[2] == False:
				ent[1].collision_started(col)
				ent[2] = True

			for j in range(col_count):
				col[j][2]["force_distribution"] = force_distribution

				for k in range(1):
					ent[1].eval_collision(col[j][1],col[j][2], dt)


		#in the fourth step we update our positions according to our values
		for i in range(len(self.physics_entities)):

			if self.physics_entities[i][1].get_name() == "RigidBody":
				self.physics_entities[i][1].update_positions(dt)
