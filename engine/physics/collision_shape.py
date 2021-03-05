from engine_math import vector3

class CollisionShape:

    def __init__(self):
        self.collision_base_points = []
        self.transformed_collision_points = []

        self.inertia_tensor = None
        self.inv_inertia_tensor = None


    def calculate_inertia_tensor(self, mass):
        pass

    def get_center_of_mass(self):
        return None

    def transform_was_changed(self, transform):
        self.transformed_collision_points = []
        matrix = transform.get_transformation_matrix()

        for i in range(len( self.collision_base_points) ):
            self.transformed_collision_points.append( matrix.mul_vec3(self.collision_base_points[i]) )

    def get_inertia_tensor(self):
        return self.inertia_tensor

    def get_inverse_inertia_tensor(self):
        return self.inv_inertia_tensor

    def get_transformed_points(self):
        return self.transformed_collision_points

    #in the future we should probably cache this
    def get_centroid(self):

        centroid = vector3.Vector3()

        for i in range(len(self.collision_base_points)):
            centroid = centroid + self.collision_base_points[i]

        centroid = centroid * len(self.collision_base_points)


        return centroid
