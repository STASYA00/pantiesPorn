import bpy

from config import PART_COLLECTION
from factory import Factory


class Panties:
    def __init__(self, name="test") -> None:
        self.name = name
        self.factory = Factory()
        self.parts = self._populate()

    def _populate(self):
        _parts = []
        for part in self.get_children():
            _parts.append(self.factory.produce(part))
        print(len(_parts))
        return _parts

    def get_children(self):
        """
        Function that returns all the attributes of the attribute group as mesh.
        return: list of objects in the group, list of mesh
        """
        return [x.name for x in bpy.data.collections[PART_COLLECTION].all_objects]

    def make(self):
        return self._make()

    def _make(self):
        for _part in self.parts:
            _part.make()
        

