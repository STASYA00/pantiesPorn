import bpy
import os

from config import IMG_SAVE, IMAGE_SIZE
from blender_utils import *
from naming import NamingProtocol

class Renderer:
    """
    Class that manages the scene rendering. Incomplete.
    """
    def __init__(self):
        self.engine = 'CYCLES'
        self.naming = NamingProtocol()
        bpy.types.ImageFormatSettings.color_mode = 'RGBA'
        self._scene_name = bpy.data.scenes[-1].name
        self.scene = bpy.data.scenes[self._scene_name]
        self.scene.render.image_settings.color_mode = 'RGBA'
        self.scene.render.resolution_percentage = 100
        self.scene.render.resolution_x = IMAGE_SIZE[0]
        self.scene.render.resolution_y = IMAGE_SIZE[1]

    def render(self, filename:str='new_mask_test'):
        """
        Function that performs all the rendering steps: normal render, segmentation
        mask.
        :param filename: name of the file, str
        :return:
        """
        deselect_all()
        self._render(filename)
        
    def _render(self, filename):
        """
        Function that renders the scene.
        :return:
        """
        image_settings = bpy.context.scene.render.image_settings
        image_settings.file_format = "PNG"
        image_settings.color_depth = '8'
        
        bpy.data.scenes[self._scene_name].render.engine = self.engine
        
        bpy.ops.render.render()
        if not IMG_SAVE in os.listdir():
            os.mkdir(IMG_SAVE)
        try:
            bpy.data.images["Render Result"].save_render(
                self.naming.filename.format(IMG_SAVE, filename))
        except RuntimeError as e:
            print(repr(e))
            print("Could not save the render {}".format(filename))
            pass

