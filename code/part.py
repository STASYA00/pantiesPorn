import bpy
import numpy as np

from colorgen import ColorGenerator
from category_picker import CategoryPicker
from condition import Condition
from material import *

class Part:
    """
    Generic class that contains a texture-customizable subpart of the main object.
    """
    def __init__(self, name) -> None:
        """
        Class initialization.
        """
        self.name = name
        self.mesh = self._load()
        self.materials = self._load_materials()
        self.active_values = []
        self.has_print = False

    def make(self):
        """
        Function that chooses a random texture and applies it to the part.
        """
        return self._make()

    def _clean_active(self):
        if not isinstance(self, TextureTrimPart):
            self.active_values = [x if isinstance(x, str) else x.name for x in self.active_values]

    def _hide(self, value=False):
        bpy.data.objects[self.name].hide_viewport = value
        bpy.data.objects[self.name].hide_render = value

    def _load(self):
        """
        Function that gets the mesh of the part.
        """
        if self.name in [x.name for x in bpy.data.objects]:
            return bpy.data.objects[self.name]
        else:
            print("ERROR:       Mesh {} was not found in the scene.".format(self.name))
            raise AttributeError

    def _load_materials(self):
        return [NonNftMaterial(self)]  #[NftMaterial(self), NonNftMaterial(self)]

    def _make(self):
        """
        Function that gets the customizable node from the part's active material tree.
        """
        
        self._reset()
        self._update_materials()
        self._clean_active()

    def _reset(self):
        self.active_values = []
        self.has_print = False

    def _update_materials(self):
        for m in self.materials:
            self.active_values += m.make()


class FabricPart(Part):
    def __init__(self, name) -> None:
        Part.__init__(self, name)
        self._picker = CategoryPicker()

    def _update_materials(self):
        category, values = self._picker.make(self)
        
        for m, val in zip(self.materials, values):
            m.has_print = self.has_print
            self.active_values += m.make(category=category, 
                                         value=val)
    
class SubstancePart(Part):
    def __init__(self, name) -> None:
        Part.__init__(self, name)
        self.has_print = True
        self._picker = CategoryPicker()
    
    def _load_materials(self):
        return [SubstanceMaterial(self)]

    def _update_materials(self):
        category, values = self._picker.make_special(self)
        for m, val in zip(self.materials, values):
            self.active_values += m.make(category=category, 
                                         value=val)

class SubstanceColorPart(SubstancePart):
    def __init__(self, name) -> None:
        SubstancePart.__init__(self, name)

    def _load_materials(self):
        return [SubstanceMaterial(self), ColorMaterial(self)]

class PatchPart(Part):
    def __init__(self, name) -> None:
        Part.__init__(self, name)
    
    def _load_materials(self):
        return [NonNftMaterial(self)]


class FurPart(Part):
    def __init__(self, name) -> None:
        Part.__init__(self, name)
        self.has_print = True

    def _load_materials(self):
        return [FurMaterial(self)]


class WaistbandPart(Part):
    def __init__(self, name) -> None:
        Part.__init__(self, name)

    def _load_materials(self):
        return [ColorMaterial(self)]

class StitchPart(Part):
    def __init__(self, name) -> None:
        Part.__init__(self, name)

    def _load_materials(self):
        return [ColorMaterial(self)]

class TrimPart(Part):
    def __init__(self, name) -> None:
        Part.__init__(self, name)

    def _load_materials(self):
        return [ColorMaterial(self)]

class TextureTrimPart(TrimPart):
    def __init__(self, name) -> None:
        Part.__init__(self, name)

    def _load_materials(self):
        return [MetalTextureMaterial(self)]


class LoopPart(TrimPart):
    def __init__(self, name) -> None:
        TrimPart.__init__(self, name)

    def _load_materials(self):
        return [SubstanceMaterial(self)]

    def _update_materials(self):
        category = self._picker.make_special(self)
        for m in self.materials:
            self.active_values+=m.make(category=category)