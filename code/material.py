import bpy
import os

from naming import NamingProtocol


class Texture:
    def __init__(self, category, name) -> None:
        self.name = name
        self.category = category
        self.name_protocol = NamingProtocol()
        self.content = self._load()

    def _load(self):
        path = os.path.dirname(__file__)[:-4]
        try:
            if not self.name in [x.name for x in bpy.data.images]:
                bpy.ops.image.open(filepath=path + self.name_protocol.material_path.format(self.category, self.name))
            else:
                print(bpy.data.images[self.name].filepath)
                path1 = bpy.data.images[self.name].filepath[4:].replace('//', '/').replace('\\\\', '/').replace('\\', '/')
                other_path = path + self.name_protocol.material_path.format(self.category, self.name)
                other_path = other_path[3:].replace('//', '/').replace('\\\\', '/').replace('\\', '/')
                if path1 != other_path:
                    bpy.data.images[self.name].filepath = path + self.name_protocol.material_path.format(self.category, self.name)
            return bpy.data.images[self.name]
            
        except Exception as e:
            print('Failed to load {} texture'.format(self.name))
            print(repr(e))
            self.current_texture = "Failed to load"

    