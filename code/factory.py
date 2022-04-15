import bpy
from part import *

class Factory:
    def __init__(self) -> None:
        self.map = {"badge": TrimPart,
                    "back_lace": SubstancePart,
                    "back_trim": SubstancePart,
                    "blob": TrimPart,
                    "chain": TrimPart,
                    "default": FabricPart,
                    "diamond": WaistbandPart,
                    "dominant": PatchPart,
                    "eyelet": TrimPart,
                    "frill": PatchPart,
                    "fur": FurPart,
                    "hem": FabricPart,
                    "link": TrimPart,
                    "loop": SubstancePart,
                    "key": TextureTrimPart,
                    "metal": TrimPart,
                    "paramline": StitchPart,
                    "patch": PatchPart,
                    "puff": StitchPart,
                    "ribbon": SubstanceColorPart,
                    "ring": TrimPart,
                    "rope": SubstancePart,
                    "silk": SubstanceColorPart,
                    "stitch": StitchPart ,
                    "strap": PatchPart,
                    "waistband": WaistbandPart,
                    "zipper": SubstancePart,
        }

    def _check_waistband(self, name):
        return "waistband" in [x.material.name.lower() for x in bpy.data.objects[name].material_slots if x.material]

    def produce(self, name):
        
        for key, value in self.map.items():
            if key in name.lower():
                if value:
                    return value(name)
                else:
                    return None
            if self._check_waistband(name):
                return self.map["waistband"](name)
        
        return self.map["default"](name)