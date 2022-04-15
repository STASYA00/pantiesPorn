import bpy
import numpy as np
import os
import sys

from config import PART_COLLECTION, MESH_NAME, LIGHT_SETUP, TRIM_COLLECTION
from controller import Controller
from factory import Factory
from log import PantiesModels
from part import TrimPart
from weights import Weights


class Panties:
    def __init__(self, name="test") -> None:
        self.name = name
        self._exclude = ["pins", "diamond"]
        self.factory = Factory()
        self.variants = self._get_variants()
        self.active_variant = self._variant()
        self.parts = self._populate()
        self.weights = Weights()
        self._controller = Controller()
        self.hasprint = self._has_print()
        self.hastrim = self._has_trim()

    def _has_print(self):
        value = np.random.random()
        return value < self.weights.get("nft")

    def _has_trim(self):
        value = np.random.random()
        return value < self.weights.get("trim")

    def get_children(self, variant=None):
        """
        Function that returns all the attributes of the attribute group as mesh.
        return: list of objects in the group, list of mesh
        """
        if not variant:
            variant = self.active_variant
        return [x.name for x in bpy.data.collections[variant].all_objects if not ("nurbs" in x.name.lower() or "bezier" in x.name.lower())]

    def get_part(self, material_name):
        try:
            if material_name.startswith("print"):
                material_name = material_name[6:]
            return [x for x in self.parts[self.active_variant] if x.mesh.active_material.name==material_name][0]
        except Exception as e:
            print(self.active_variant)
            print(material_name, [x.mesh.active_material.name for x in self.parts[self.active_variant]])
            print([x for x in self.parts[self.active_variant] if material_name[6:] in x])
            print(repr(e))
            raise KeyboardInterrupt

    def make(self):
        return self._make()

    def _activate_variant(self):
        for _v in self.variants:
            value = True
            if _v == self.active_variant:
                value = False
            for c in [_v, LIGHT_SETUP + "_" + _v[-2:]]:  # add light setup collection to this list
                bpy.data.collections[c].hide_viewport = value
                bpy.data.collections[c].hide_render = value

    def _check_produce(self, value):
        for _excl in self._exclude:
            if _excl in value.lower():
                return False
        return True

    def _get_variants(self):
        return [x.name for x in bpy.data.collections if x.name.startswith(MESH_NAME) and LIGHT_SETUP not in x.name]

    def _hide_trim(self, value=False):
        trims = [x.name for x in bpy.data.collections[self.active_variant].children \
            if x.name.lower().startswith(TRIM_COLLECTION.lower())]
        if len(trims) > 0:
            for trim in trims:
                bpy.data.collections[trim].hide_viewport = value
                bpy.data.collections[trim].hide_render = value

    def _make(self):
        #rewrite REWRITE
        self.active_variant = self._variant()
        self._activate_variant()
        self.hasprint = self._has_print()
        printed_part = self._set_print()
        self.hastrim = self._has_trim()
        self._hide_trim(value=not self.hastrim)
        
        for _part in self.parts[self.active_variant]:
            if _part.name == printed_part:
                _part.has_print = True
            if isinstance(_part, TrimPart):
                if not self.hastrim:
                    _part.active_values = ["hidden"]
                    continue
            _part.make()
            
        self._controller.make(self)
        return LIGHT_SETUP + "_" + self.active_variant[-2:]

    def _name_model(self):
        model = bpy.data.filepath.split(".")[-2][-4]
        return PantiesModels().get(model)

    def _populate(self):
        _parts = {}
        for variant in self.variants:
            _parts[variant] = []
            _materials = []
            
            for part in self.get_children(variant):
                try:
                    if bpy.data.objects[part].active_material.name not in _materials:
                        if self._check_produce(bpy.data.objects[part].active_material.name.lower()):  # quick fix - refactor
                            _materials.append(bpy.data.objects[part].active_material.name)
                            _new_part = self.factory.produce(part)
                            if _new_part:
                                _parts[variant].append(_new_part)
                except Exception:
                    pass
        return _parts

    def _set_print(self):
        if self.hasprint and self._name_model().lower()!="paris":
            rel_parts = [x for x in self.parts[self.active_variant]]
            printed_part = np.random.choice(rel_parts, 1)[0].name
            return printed_part

    def _variant(self, var_ind=None):
        if not var_ind:
            return np.random.choice(self.variants, 1)[0]
        else:
            var_ind = max(0, min(var_ind, len(self.variants)))
            return self.variants[var_ind]

    

    
        

