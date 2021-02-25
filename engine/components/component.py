

class Component:

    def __init__(self):
        self.attached_entity = None

    def set_attached_to(self, entity):
        self.attached_entity = entity

    def initialize(self):
        pass

    def get_name(self):
        return "Component"

    def update(self, dt):
        pass

    def fixed_update(self, dt):
        pass

    def render(self, camera, shader):
        pass

    def transform_was_modified(self, transform):
        pass
