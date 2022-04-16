import bpy
import numpy as np
import os

from colorgen import ColorGenerator
from condition import Condition
from materialfactory import TextureFactory
from materialdictionary import SubstanceDictionary
from blender_utils import get_fromnode_links, get_nodes_link, get_tonode_links
    
class Material:
    def __init__(self, part):
        self.part = part
        self.factory = TextureFactory()
        self.has_print = ""
        self._nodes = self._get_node()
        self.colorgen = None
        self._suffix = "NFT"
        self.active_values = []
        
    def activate(self):
        pass

    def make(self, category="random", value=True):
        return self._make(category, value)

    def _get_node(self):
        """
        Function that gets the customizable node from the part's active material tree.
        """
        m = [x.material for x in self.part.mesh.material_slots if x.material][0]
        return [x for x in m.node_tree.nodes if self._get_nodename() in x.name]

    def _get_nodename(self):
        return "Image Texture"  # "RGB"

    def _make(self, category, value=True):
        self._reset()
        if value:
            self.activate()
            self.active_values = self._produce_textures(category)
            self._update_nodes(self.active_values)
        return self.active_values

    def _produce_textures(self, category=None):
        return []

    def _reset(self):
        self.active_values = []

    def _split_nodes(self, material):
        print("Material {} in object {} should not be split.".format(
            self.part.mesh.active_material, self.part.name))
        raise KeyboardInterrupt
    
    def _update_nodes(self, materials):
        pass


class SubstanceMaterial(Material):
    def __init__(self, part):
        Material.__init__(self, part)
        self.mapdict = SubstanceDictionary()

    def activate(self):
        _current_material = self.part.mesh.active_material.name
        try:
            if not self._suffix in _current_material:
                self.part.mesh.active_material = bpy.data.materials[
                    _current_material + "_" + self._suffix]
                    
        except KeyError:
            print("Could not activate material {} as NFT".format(_current_material))
            pass

    def _get_links(self):
        """
        Function that gets the main node from the part's active material tree.
        """
        m = [x.material for x in self.part.mesh.material_slots if x.material][0]
        return [x for x in m.node_tree.links]

    def _produce_textures(self, category):
        self.active_values.append(category)
        _result = self.factory.produce_substance(category)
        return _result

    def _check_link(self, link):
        for key, value in self.mapdict.content.items():
            if link.to_node.name.lower() == key.lower():
                for v in value:
                    if link.to_socket.name.lower() == v[0].lower():
                        return v[1]

    def _update_nodes(self, materials):
        _result = materials
        self._nodes = self._get_node()
        for n in self._nodes:
            mapname = None
            links = get_fromnode_links(n, self._get_links())
            for link in links:
                mapname = self._check_link(link)
                
                if mapname:
                    if mapname.lower() != "print".lower(): 
                        texture = [x for x in _result if mapname.lower() in x.name.lower()]
                        
                        if texture:
                            texture = texture[0]
                            n.image = texture.content


class NftMaterial(SubstanceMaterial):
    def __init__(self, part):
        SubstanceMaterial.__init__(self, part)

    def activate(self):
        _current_material = self.part.mesh.active_material.name
        try:
            if not self._suffix in _current_material:
                self.part.mesh.active_material = bpy.data.materials[
                    _current_material + "_" + self._suffix]
                    
        except KeyError:
            print("Could not activate material {}".format(_current_material))
            pass

    def _produce_textures(self, category):
        self.active_values.append(category)
        _result = self.factory.produce_substance(category)
        nft_print = self.factory.produce(self.has_print, texture_type=2)[0]
        return _result, nft_print

    def _update_nodes(self, materials):
        
        self._reset()
        _result, nft_print = materials
        self._nodes = self._get_node()
        for n in self._nodes:
            mapname = None
            links = get_fromnode_links(n, self._get_links())
            for link in links:
                mapname = self._check_link(link)
                if mapname:
                    if mapname.lower() != "print".lower():
                        texture = [x for x in _result if mapname.lower() in x.name.lower()][0]
                    else:
                        texture = nft_print
                        self.active_values.append(nft_print)
                    n.image = texture.content
                    

class FurMaterial(Material):
    def __init__(self, part):
        Material.__init__(self, part)

    def _produce_textures(self, category):
        _exception = []
        texture = self.factory.produce(category, 
                                             exception=_exception, 
                                             texture_type=1)[0]
        #self.active_values.append(print_texture)
        return [texture]

    def _produce_print_textures(self, category):
        _exception = []
        print_texture = self.factory.produce(category, 
                                             exception=_exception, 
                                             texture_type=2)[0]
        #self.active_values.append(print_texture)
        return [print_texture]

    def _update_nodes(self, materials):
        texture = materials[0]
        for n in self._nodes:
            n.image = texture.content


class MetalTextureMaterial(Material):
    def __init__(self, part):
        Material.__init__(self, part)

    def _produce_textures(self, category=None):
        mat = self.part.mesh.active_material.name
        return self.factory.produce(mat, texture_type=3)

    def _update_nodes(self, materials):
        texture = materials[0]
        for n in self._nodes:
            n.image = texture.content
        self.active_values = []


class NonNftMaterial(Material):
    def __init__(self, part):
        Material.__init__(self, part)

    def activate(self):
        _current_material = self.part.mesh.active_material.name
        try:
            if self._suffix in _current_material:
                self.part.mesh.active_material = bpy.data.materials[
                    _current_material[:-(len(self._suffix)+1)]]
                    
        except KeyError:
            print("Could not activate material {}".format(_current_material))
            pass

    def _fix_nodes(self):
        bump_nodes = [x for x in self.part.mesh.active_material.node_tree.nodes if "bump" in x.name.lower()]
        disp_nodes = [x for x in self.part.mesh.active_material.node_tree.nodes if "displacement" in x.name.lower()]
        if len(bump_nodes)>0:
            bump_nodes[0].inputs[0].default_value = 0.1
        if len(disp_nodes)>0:
            _links = self.part.mesh.active_material.node_tree.links
            img_node = get_tonode_links(disp_nodes[0], _links)[0].from_node
            img_node.image.colorspace_settings.name = "Non-Color"
        self.part.mesh.active_material.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.6

    def _get_node(self):
        """
        Function that gets the customizable node from the part's active material tree.
        """
        
        for m in [x.material for x in self.part.mesh.material_slots if x.material]:
            _nodes_of_interest = [x for x in m.node_tree.nodes if self._get_nodename() in x.name]
            if len(_nodes_of_interest) > 1:
                _node, _disp_node, _print_node = self._split_nodes(m)
                return [_node, _disp_node, _print_node]
        return [_nodes_of_interest[0]]

    def _produce_print(self):
        if self.has_print:
            
            return self.factory.produce(self.has_print, texture_type=2)
        return [None]

    def _produce_textures(self, category):
        _result = []
        _exception = []
        if "dominant" in self.part.name.lower():
            return self.factory.produce_special(self.part.name)
        _result += self.factory.produce(category, exception=_exception)
        _result += self._produce_print()
        
        return [x for x in _result]

    def _update_nodes(self, textures):
        self._reset()
        self._nodes = self._get_node()
        material = textures[0]
        # update the main material node
        self._nodes[0].image = material.content
        self.active_values.append(material)

        # update the displacement node
        disp_on = False
        if textures[1]:
            disp_on = True
        #self._update_value(which=1, on=disp_on)
        if disp_on:
            self._nodes[1].image = textures[1].content
            self._update_height(textures[1])
            self._fix_nodes()
        #self._control_mix_nodes()

        # update the print node
        self._update_value(on=True)
        if self.has_print:
            self._update_value(on=False)
            print_texture = textures[2]
            if print_texture:
                if len(self._nodes) > 1 and self.has_print:
                    self._nodes[-1].image = print_texture.content
                    self.active_values.append(print_texture)
                    return

    def _control_mix_nodes(self):
        nodes = [x for x in self.part.mesh.active_material.node_tree.nodes if "mix" in x.name.lower()]
        for n in nodes:
            for i in range(3):
                n.inputs["Color1"].default_value[i] = 0

    def _split_nodes(self, material):
        _links = [x for x in material.node_tree.links if x.from_node.name.startswith("Image Texture")]
        node, disp_node, print_node = None, None, None
        for link in _links:
            if link.to_socket.name in ["Value", "Color1", "Color"]:
                print_node = link.from_node
            if link.to_socket.name in ["Alpha", "Color2"]:
                node = link.from_node
            if link.to_socket.name == "Height":
                disp_node = link.from_node
            
        if node == print_node:
            print_node = None
        return node, disp_node, print_node

    def _update_height(self, texture):
        value = 0.00025
        if texture.category.split("/")[1].lower() == "terry":
            value = 0.002
        elif texture.name == "Lace_Regular_06":
            value = 0.002
        node = [x for x in self.part.mesh.active_material.node_tree.nodes if "Displacement" in x.name]
        
        if len(node) > 0:
            node = node[0]
            node.inputs[2].default_value = value

    def _update_value(self, which=0, on=True):
        
        _nodes = [x for x in self.part.mesh.active_material.node_tree.nodes if "Mix" in x.name]
        sockets = ["Base Color"]
        if which == 1:
            sockets = ["Normal", "Displacement"]
        if len(_nodes) > 0:
            _links = [x for x in self.part.mesh.active_material.node_tree.links if x.from_node.name.startswith("Mix")]
            for socket in sockets:
                for link in _links:
                    
                    if link.to_socket.name == socket:
                        _node = link.from_node
                        _node.inputs[0].default_value = on


class ColorMaterial(Material):
    def __init__(self, part):
        Material.__init__(self, part)
        self.colorgen = ColorGenerator()

    def _get_nodename(self):
        return "RGB"

    def _get_node(self):
        """
        Function that gets the customizable node from the part's active material tree.
        """
        m = [x.material for x in self.part.mesh.material_slots if x.material][0]
        return [x for x in m.node_tree.nodes if self._get_nodename() in x.name and "BW" not in x.name]

    def _produce_textures(self, category=None):
        _color = self.colorgen.make()
        #self.active_values.append(_color)
        return [_color]

    def _update_nodes(self, materials):
        _color = materials[0]
        for _node in self._nodes:
            for i, c in enumerate(_color.values):
                _node.outputs[0].default_value[i] = c

