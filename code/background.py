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
        self.content = self._get_mesh()
        self._node_value = self.content.node_tree.nodes["Image Texture"]
        self._factory = TextureFactory()

    def make(self, color=None, exception=None):
        """
        Function that assigns a color to the background. In case no color is given
        the color is chosen randomly from colors.csv.
        :param: color          color to assign to the background, set of floats (r, g, b)
        :param: exception      color not to have in the texture assigned to the background, str
        """
        return self._make(color, exception)

    def _get_mesh(self):
        """
        Function that gets the object that is considered to act as a background.
        returns: background object, bpy mesh
        """
        return bpy.data.materials[BGR_NAME]

    def _make(self, color=None, exception=None):
        """
        Function that assigns a color to the background. In case no color is given
        the color is chosen randomly from colors.csv.
        :param: color          color to assign to the background, set of floats (r, g, b)
        :param: exception      color not to have in the texture assigned to the background, str
        """
        
        texture = self._factory.produce("bgr")[0]
        if exception:
            while exception in texture.name:
                texture = self._factory.produce("bgr")[0]
                
        self._node_value.image = texture.content
        #return texture - for image input in light
        return texture.name.split(".")[0]  #texture.name.split("_")[1]