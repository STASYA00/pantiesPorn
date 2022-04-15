import bpy
import numpy as np

from config import CAMERA

class CameraManager:
    def __init__(self) -> None:
        self.cameraname = CAMERA
        self.cam = self._get_cam()
        if self.cam:
            self.position = self.cam.location
            self._init_angle = self.cam.rotation_euler
            self.min_angle = -10
            self.max_angle = 10
            try:
                bpy.data.objects["Camera"].constraints["Track To"].use_target_z = True
            except Exception:
                pass

    def make(self):
        return self._make()

    def _get_angle(self):
        return np.random.randint(self.min_angle, self.max_angle) + \
                                    np.random.random()

    def _get_cam(self):
        try:
            return [x for x in bpy.data.objects if self.cameraname in x.name][0]
        except IndexError:
            print("No camera {} detected in the scene".format(CAMERA))

    def _get_dims(self):
        dims = np.random.choice([0, 1, 2], np.random.choice(list(range(4)), 1)[0])
        return dims

    def _make(self):
        if self.cam:
            self._reset()
            self._rotate()

    def _rotate(self, angle=None):
        
        for dim in self._get_dims():
            angle = self._get_angle()
            self.cam.rotation_euler[dim] = np.radians(angle)

    def _reset(self):
        self.cam.location = self.position
        self.cam.rotation_euler = self._init_angle
