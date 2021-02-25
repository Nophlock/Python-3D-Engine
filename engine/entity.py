
from transform import Transform

class Entity:

    def __init__(self):
        self.transform = Transform(self)
        self.components = {}

        self.children = []
        self.parent = None



    def get_transform(self):
        return self.transform

    def add_component(self, comp):
        comp.set_attached_to(self)
        self.components[comp.get_name()] = comp

        comp.initialize()
        comp.transform_was_modified(self.transform)

    def get_component(self, name):
        return self.components[name]


    def add_child(self, child):
        self.children.append(child)
        self.transform.add_child(child)

        child.parent = self

    def remove_child(self, child):

        if child.parent != self:
            return

        self.children.remove(child)
        self.transform.remove_child(child)

        child.parent = None

    def transform_was_modified(self):

        for comp_name in self.components:
            self.components[comp_name].transform_was_modified(self.transform)


    def update(self, dt):

        for comp_name in self.components:
            self.components[comp_name].update(dt)


    def fixed_update(self, dt):

        for comp_name in self.components:
            self.components[comp_name].fixed_update(dt)

    def render(self, camera, shader):

        for comp_name in self.components:
            self.components[comp_name].render(camera, shader)
