
from physics		import gjk
from physics		import epa

class PhysicsEngine:

    def __init__(self, scene_mgr):
        self.scene_mgr = scene_mgr
        self.physics_entities = []
        self.collided_entities = []


    def add_physics_object(self, entity, resolver):
        self.physics_entities.append([entity, resolver])


    def fixed_update(self, dt):


        for i in range( len(self.physics_entities) ):

            comp = self.physics_entities[i][1]
            aabb = comp.get_collision_aabb()

            for j in range( len(self.physics_entities) ):

                if i == j:
                    continue

                o_comp = self.physics_entities[j][1]
                o_aabb = o_comp.get_collision_aabb()


                if aabb.is_aabb_inside_aabb(o_aabb):

                    poly_a = self.physics_entities[i][1].get_collision_polygon()
                    poly_b = self.physics_entities[j][1].get_collision_polygon()

                    col, simplex = gjk.GJK.is_polygon_colliding(poly_a, poly_b)

                    if col:

                        pack = [ self.physics_entities[i], self.physics_entities[j] ]

                        if pack not in self.collided_entities:
                            self.physics_entities[i][1].collision_started(self.physics_entities[j])
                            self.physics_entities[j][1].collision_started(self.physics_entities[i])

                            self.collided_entities.append([ self.physics_entities[i], self.physics_entities[j] ])

                        min_normal, min_distance = epa.EPA.get_penetration_data(simplex, poly_a, poly_b)
                        self.physics_entities[i][1].eval_collision(self.physics_entities[j], min_normal, min_distance)


                else:
                    pack = [ self.physics_entities[i], self.physics_entities[j] ]

                    if pack in self.collided_entities:
                        pack[0][1].collision_stopped(pack[1])
                        pack[1][1].collision_stopped(pack[1])
                        self.collided_entities.remove(pack)
