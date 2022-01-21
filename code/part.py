import bpy

from colorgen import ColorGenerator
from materialfactory import TextureFactory

class Part:
    """
    Generic class that contains a texture-customizable subpart of the main object.
    """
    def __init__(self, name) -> None:
        """
        Class initialization.
        """
        self.name = name
        self._nodename = self._get_nodename()
        self.mesh = self._load()
        self.factory = TextureFactory()
        self._nodes = self._get_node()

    def make(self, category="random"):
        """
        Function that chooses a random texture and applies it to the part.
        """
        return self._make(category)

    def _get_node(self):
        """
        Function that gets the customizable node from the part's active material tree.
        """
        _nodes = []
        for m in [x.material for x in self.mesh.material_slots]:
            _nodes.append([x for x in m.node_tree.nodes if self._nodename in x.name][0])
        return _nodes

    def _get_nodename(self):
        return "Image Texture"

    def _load(self):
        """
        Function that gets the mesh of the part.
        """
        if self.name in [x.name for x in bpy.data.objects]:
            return bpy.data.objects[self.name]
        else:
            print("ERROR:       Mesh {} was not found in the scene.".format(self.name))
            raise AttributeError

    def _make(self, category="random"):
        """
        Function that gets the customizable node from the part's active material tree.
        """
        _material = self.factory.produce(category)
        for _node in self._nodes:
            _node.image = _material.content


class FurPart(Part):
    def __init__(self, name) -> None:
        Part.__init__(self, name)
        self.colorgen = ColorGenerator()

    def _get_nodename(self):
        return "RGB"

    def _make(self, category="random"):
        _color = self.colorgen.make()

        for _node in self._nodes:
            for i, c in enumerate(_color):
                _node.outputs[0].default_value[i] = c


class StitchPart(Part):
    def __init__(self, name) -> None:
        self._nodename = "Principled BSDF"
        Part.__init__(self, name)
        self.colorgen = ColorGenerator()

    def _make(self, category="random"):
        _color = self.colorgen.make()
        for _node in self._nodes:
            for i, c in enumerate(_color):
                _node.inputs[0].default_value[i] = c
    