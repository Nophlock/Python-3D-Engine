import os

from mesh_loaders import iqm_loader
from mesh_loaders import obj_mesh_loader


class MeshLoader:

    def __init__(self, scene_mgr):
        self.extension = {}
        self.scene_mgr = scene_mgr

        self.extension["iqm"] = iqm_loader.IQMLoader(scene_mgr)
        self.extension["obj"] = obj_mesh_loader.OBJMeshLoader(scene_mgr)


    def get_meshs(self, file_path):
        file_name, file_extension = os.path.splitext(file_path)
        file_extension = file_extension[1:]

        if file_extension in self.extension:
            return self.extension[file_extension].get_meshs(file_path)
        else:
            print("Warning unknown model-extension: ", file_path)
            return None
