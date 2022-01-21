import bpy
import os
import sys

from material import Texture
from materialdictionary import MaterialDictionary
from naming import NamingProtocol

# from config import SCRIPT_PATH

# sys.path.append(SCRIPT_PATH)

import numpy as np

class TextureFactory:
    def __init__(self) -> None:
        self._naming = NamingProtocol()
        self._d = MaterialDictionary()

    def produce(self, fabric):
        return self._produce(fabric)

    def _produce(self, fabric):
        _category = self._d.get(fabric)
        _fab = np.random.choice(os.listdir(self._naming.material_path.format(_category, "")), 1)[0]
        return Texture(_category, _fab)
        