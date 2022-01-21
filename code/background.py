import bpy

from config import BGR_NAME
from materialfactory import TextureFactory


class Background:
    """
    Class that stores and manages the background of the scene.
    """
    def __init__(self) -> None:
        """
        Class initialization.
        """
        self.mesh = self._get_mesh()
        self._node_value = self.mesh.active_material.node_tree.nodes["Image Texture"]
        self._factory = TextureFactory()

    def make(self, color=None):
        """
        Function that assigns a color to the background. In case no color is given
        the color is chosen randomly from colors.csv.
        :param: color          color to assign to the background, set of floats (r, g, b)
        """
        return self._make(color)

    def _get_mesh(self):
        """
        Function that gets the object that is considered to act as a background.
        returns: background object, bpy mesh
        """
        return bpy.data.objects[BGR_NAME]

    def _make(self, color=None):
        """
        Function that assigns a color to the background. In case no color is given
        the color is chosen randomly from colors.csv.
        :param: color          color to assign to the background, set of floats (r, g, b)
        """
        
        self._node_value.image = self._factory.produce("bgr").content