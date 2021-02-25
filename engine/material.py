

class Material:

    def __init__(self):
        self.data = {}

        self.data["mesh_color"] = [1.0, 1.0, 1.0, 1.0]


    def assign_material(self, index, value):
        self.data[index] = value

    def get_material_data(self):
        return self.data

    def get_copy(self):
        mat = Material()

        for name in self.data:
            mat.data[name] = self.data[name]

        return mat
