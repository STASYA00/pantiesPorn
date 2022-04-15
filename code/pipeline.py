import bpy
import os
import sys


file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
from background import Background
from cameramanager import CameraManager
from config import BLEND_DIR
from light import LightSetup
from log import Log
from mood_calculator import MoodCalculator
from panties import Panties
from renderer import Renderer
from tracker import Tracker


class Pipeline:
    """
    Generic pipeline class.
    """
    def __init__(self, value: int) -> None:
        """
        Class initialization.
        :param: value       value, int
        """
        self.value = value

    def run(self):
        """
        Function that executes the pipeline.
        """
        return self._run()

    def _run(self):
        """
        Function that executes the pipeline.
        """
        return 0


class RenderPipeline(Pipeline):
    """
    Pipeline that creates different character configurations.
    """
    def __init__(self, value: int) -> None:
        """
        Class initialization.
        :param value        character configuration number to reproduce, int.
        """
        super().__init__(value)

    def _run(self):
        """
        Function that creates a character configuration from a number of parameters.
        """
        renderer = Renderer()
        renderer.render(filename="1" + str(self.value))


class MainPipeline(Pipeline):
    """
    Pipeline that creates different character configurations.
    """
    def __init__(self, value: int) -> None:
        """
        Class initialization.
        :param value        amount of character configurations to create, int.
        """
        super().__init__(value)

    def run(self, val=0):
        return self._run(val)

    def _run(self, current_frame=1):
        """
        Function that creates different character configurations.
        """
        total_frames = self.value + current_frame
        background = Background()
        character = Panties()
        renderer = Renderer()
        mood = MoodCalculator()
        cam = CameraManager()
        light = LightSetup()
        log = Log()
        tracker = Tracker(character)
        
        while current_frame < total_frames:
            print(f"EPOCH {current_frame} OUT OF {self.value}")
            l = character.make()
            
            approve, color = mood.make(character)
            if approve:
                tex = background.make(exception=color)
                light.make(l, tex)
                #cam.make()
                if tracker.make(character):
                    log.make(str("%04d" % current_frame), tracker.get())
                    #renderer.render(filename=str("%04d" % current_frame))
                    log.save()
                    current_frame+=1

                    # DEBUG
                    # if not BLEND_DIR in os.listdir():
                    #     os.mkdir(BLEND_DIR)
                    # bpy.ops.wm.save_as_mainfile(filepath='{}.blend'.format(str(i)))
        tracker.tree.show()
        tracker.export()

