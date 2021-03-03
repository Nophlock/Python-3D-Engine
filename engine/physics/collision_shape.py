

class CollisionShape:

    def __init__(self):
        self.collision_base_points = []
        self.transformed_collision_points = []


    def get_center_of_mass(self):
        return None

    def transform_was_changed(self, transform):
        self.transformed_collision_points = []
        matrix = transform.get_transformation_matrix()

        for i in range(len( self.collision_base_points) ):
            self.transformed_collision_points.append( matrix.mul_vec3(self.collision_base_points[i]) )


    def get_transformed_points(self):
        return self.transformed_collision_points
