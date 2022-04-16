import bpy
import os

from config import OUTPUT_FOLDER, IMAGE_SIZE, ENGINE, SAMPLES
from blender_utils import *
from log import PantiesModels
from naming import NamingProtocol

class Renderer:
    """
    Class that manages the scene rendering. Incomplete.
    """
    def __init__(self):
        self.engine = ENGINE
        self.naming = NamingProtocol()
        bpy.types.ImageFormatSettings.color_mode = 'RGBA'
        self._scene_name = bpy.data.scenes[-1].name
        self.scene = bpy.data.scenes[self._scene_name]
        self._set_gpu()
        self.scene.render.engine = self.engine
        self.scene.cycles.device = "GPU"
        self.scene.render.use_persistent_data = True
        
        self.scene.render.resolution_percentage = 100
        self.scene.render.resolution_x = IMAGE_SIZE[0]
        self.scene.render.resolution_y = IMAGE_SIZE[1]
        self.scene.cycles.samples = SAMPLES

    def render(self, filename:str='new_mask_test'):
        """
        Function that performs all the rendering steps: normal render, segmentation
        mask.
        :param filename: name of the file, str
        :return:
        """
        deselect_all()
        self._render(filename)

    def _set_gpu(self):
         pref = bpy.context.preferences.addons["cycles"].preferences
         pref.get_devices()
         gpu_dev = [x for x in pref.devices if x.type=="CUDA"][0]
         pref.compute_device_type = gpu_dev.type
         gpu_dev.use = True

    def _set_img_settings(self):
        image_settings = bpy.context.scene.render.image_settings
        image_settings.file_format = "PNG"
        image_settings.color_depth = '8'
        image_settings.color_mode = 'RGBA'

        
    def _render(self, filename):
        """
        Function that renders the scene.
        :return:
        """
        self._set_img_settings()
        
        bpy.data.scenes[self._scene_name].render.engine = self.engine
        
        bpy.ops.render.render()
        d = PantiesModels()
        print(f"output folder: {OUTPUT_FOLDER}")
        if not OUTPUT_FOLDER in os.listdir():
            os.mkdir(OUTPUT_FOLDER)
        model = bpy.data.filepath.split(".")[-2][-4]
        model = d.get(model)
        # if model not in os.listdir(OUTPUT_FOLDER):
        #     os.mkdir(f'{OUTPUT_FOLDER}/{model}')
        try:
            bpy.data.images["Render Result"].save_render(
                self.naming.filename.format(filename))
            print(f"Image saved as {self.naming.filename.format(filename)}")
        except RuntimeError as e:
            print(repr(e))
            print("Could not save the render {}".format(filename))
            pass

