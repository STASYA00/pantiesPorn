import bpy
import os

from naming import NamingProtocol


class Texture:
    def __init__(self, category, name) -> None:
        self.name = name
        self.category = category
        self.name_protocol = NamingProtocol()
        self.path = self._full_path()
        self.content = self._load()

    def is_lace(self):
        return "lace" in self.name.lower()

    def _relevant_image(self):
        relevant_names = [x.name for x in bpy.data.images if self.name in x.name]
        if len(relevant_names) > 0:
            return relevant_names[0]


    def _full_path(self):
        path = os.path.dirname(__file__)[:-4]
        return path + self.name_protocol.material_path.format(self.category, self.name)

    def _load(self):
        try:
            if not self._relevant_image():
                bpy.ops.image.open(filepath=self.path)
            else:
                self.name = self._relevant_image()
                path1 = bpy.data.images[self.name].filepath.replace('//', '/').replace('\\\\', '/').replace('\\', '/')
                other_path = self.path
                other_path = other_path[3:].replace('//', '/').replace('\\\\', '/').replace('\\', '/')
                if path1 != other_path:
                    bpy.data.images[self.name].filepath = self.path
            return bpy.data.images[self.name]
            
        except Exception as e:
            print('Failed to load {} texture'.format(self.name))
            print([x.name for x in bpy.data.images])
            print(self.name)
            print(self.path)
            print(repr(e))
            self.current_texture = "Failed to load"
