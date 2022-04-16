import bpy
import os
import sys

from config import TEXTURES, DISPLACEMENT_FOLDER
from texture import Texture
from materialdictionary import MaterialDictionary
from naming import NamingProtocol

# from config import SCRIPT_PATH

# sys.path.append(SCRIPT_PATH)

import numpy as np

class TextureFactory:
    def __init__(self) -> None:
        self._naming = NamingProtocol()
        self._d = MaterialDictionary()

    def produce_special(self, fabric)->Texture:
        textures = []
        mat = self._naming.matfolders[1]
        category, fabric = self._d.get_special(fabric)
        mat = mat + "/" + category
        textures.append(Texture(mat, fabric))
        _displacement_texture = None
        
        if category.lower() != "background":
            _displacement_texture = self._produce_disp(mat, fabric)
        textures.append(_displacement_texture)
        textures.append(None)
        return textures

    def produce(self, fabric, texture_type=1, 
                exception=[]) -> list:
        if texture_type == 1:
            return self._produce(fabric, exception)
        elif texture_type == 2:
            return self._produce_print(fabric)
        elif texture_type == 3:
            return self._produce_metal_texture(fabric)
        else:
            raise AttributeError

    def produce_substance(self, category, exception=[])->list:
        mat = self._naming.matfolders[0]
        mat_folder = self._naming.material_path.format(mat + "/" + category, "")
        fab = np.random.choice(os.listdir(mat_folder), 1)[0]
        textures = []
        for t in os.listdir(mat_folder + "/" + fab):
            # if t is an imagefile
            textures.append(Texture(mat + "/" + category + "/"+ fab, t))
        return textures

    def _produce(self, fabric, exception=["fuzz"])->list:
        textures = []
        mat = self._naming.matfolders[1]
        category = self._d.get(fabric, exception=exception)
        mat = mat + "/" + category
        check_dir = self._naming.material_path.format(mat, "")
        _options = [x for x in os.listdir(check_dir) if not os.path.isdir(f'{check_dir}/{x}')]
        fabric = np.random.choice(_options, 1)[0]
        textures.append(Texture(mat, fabric))

        # produce displacement texture
        _displacement_texture = None
        if category.lower() != "background":
            _displacement_texture = self._produce_disp(mat, fabric)
            
        textures.append(_displacement_texture)
        return textures

    def _produce_disp(self, mat, fabric) -> Texture:
        
        fabric = fabric.split(".")[-2] + "_D.png"
        folder = os.path.dirname(__file__)[:-4] + self._naming.displacement.format(mat, "")
        
        if fabric in os.listdir(folder):
            try:
                return Texture(mat + f'/{DISPLACEMENT_FOLDER}', fabric)
            except Exception as e:
                print(repr(e))
        else:
            print(f"DISPLACEMENT MAP {fabric} NOT IN FOLDER {folder}")

    def _produce_print(self, nft)->list:
        textures=[]
        mat = f'{TEXTURES}/{self._naming.matfolders[2]}'  # "NFT"
        nfts = [x for x in os.listdir(mat) if not os.path.isdir(f'{mat}/{x}') if nft.lower() in x.lower()]
        _nft = np.random.choice([x for x in os.listdir(mat) if not os.path.isdir(f'{mat}/{x}')],1)[0]
        if len(nfts) > 0:
            _nft = nfts[0]
        textures.append(Texture(self._naming.matfolders[2], _nft))
        return textures

    # def _produce_print_old(self)->list:
    #     textures = []
    #     mat = self._naming.matfolders[2]  # "NFT"
    #     folder = np.random.choice([x for x in os.listdir(TEXTURES + 
    #                                                 "/" + mat) if os.path.isdir(TEXTURES + 
    #                                                 "/" + mat + "/" + x)], 1)[0]
    #     fab = np.random.choice([x for x in os.listdir(TEXTURES + 
    #                                                 "/" + mat + "/" + folder) if "." in x], 1)[0]  # filename
    #     textures.append(Texture(mat + "/" + folder, fab))
    #     return textures

    def _produce_metal_texture(self, name)->list:
        textures = []
        fabric = self._d.get_special(name)
        textures.append(Texture(self._naming.trim, fabric[1]))
        textures.append(None)
        textures.append(None)
        return textures


        