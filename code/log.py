import bpy
import json
import os
from unicodedata import name
import sys

from config import SCRIPT_PATH
sys.path.append(SCRIPT_PATH)
from nft_generator import NftParser


import pandas as pd

from config import TEXTURES, JSON
from naming import NamingProtocol

# TODO:

# Patches / Dominants behöver byta namn på blend filerna
# diamond pantie

# DONE: name of the panties' model (typ Rose)
# DONE: number of parts
# DONE: upcycled nft name
# DONE: upcycled nft author / owner
# DONE: fabric type: color (one per pantie)
# DONE: type: Twill, value: Blue 
# DONE: type: Lace, value: someValue
# DONE: Trim : has / doesnt have
# DONE: Patch: heart / flower / smth else TODO: name the patches in the blend file

# state: 1,2,3 (make some more probable)
# 

# check the rarest values if conflict 

# TODO: check resolution with Jens : asked

class PantiesModels:
    def __init__(self) -> None:
        self._content = {1: "Erykah",
                         2: "Paris",
                         3: "Lena",
                         4: "Vivienne",
                         5: "Oprah",
                         6: "Madonna",
                         7: "Lizzo",
                         8: "Robyn", 
                         9: "Frida"
                        }
    def get(self, ind):
        return self._content[int(ind)]

class Log:

    def __init__(self):
        self.content = self._structure()
        if not JSON in os.listdir():
            os.mkdir(JSON)

    def make(self, name, attributes, bgr):
        return self._make(name, attributes, bgr)

    def reset(self):
        self.content = self._structure()

    def save(self):
        js = self.content
        filename = self._get_name()
        with open(filename, "w") as f:
            f.write(json.dumps(js, indent=4))

    def _add_attr(self, key, value):
        self.content["attributes"].append(self._attr(key, value))

    def _add_attributes(self, attributes):
        _attr_collection = LogAttributeFactory().produce()
        for attr in _attr_collection:
            result =attr.get(attributes)
            if result:
                if result!="None":
                    self._add_attr(attr.name, attr.get(attributes))

    def _attr(self, key, value):
        return {"trait_type": key, "value": value}

    def _get_name(self):
        if self.content["name"]:
            return JSON + "/" + self.content["name"][self.content["name"].index("#")+1:].rjust(4, "0") + ".json"
        return JSON + "/" + "test.json"

    def _make(self, name, attributes, bgr):
        attributes["bgr"] = bgr
        print(attributes)
        self.reset()
        self.content["name"] = f"Cryptopanties #{int(name)+1}"
        self.content["image"] = name + ".png"
        self.content["properties"]["files"][0]["uri"] = name + ".png"
        self._add_attributes(attributes)

    def _structure(self):
        return {
            "name": "",
            "symbol": "CPRR",
            "description": "CryptoPanties by Rave Review.",
            "seller_fee_basis_points": 666,
            "image": "",
            "attributes": [],
            "properties": {
                "creators": [{"address": "", "share": 100}],
                "files": [{"uri": "", "type": "image/png"}]
            },
            "collection": {"name": "Cryptopanties by Rave Review", "family": "Rave Review"}
}

class LogAttributeFactory:
    def __init__(self) -> None:
        self._attributes = {"Upcycled NFT": NftLogAttribute, 
                            "NFT Author": NftAuthorLogAttribute,
                            "Identity": PantiesModelLogAttribute,
                            "Background": BgrAttribute,
                            #"Parts": PartNumberLogAttribute,
                            #"Trim": TrimLogAttribute      
        }
        self._naming = NamingProtocol()
        self._db = TextureLogReplacement()
        self._parser = NftParser()
        self._get_fabric_attrs()


    def produce(self):
        _attribute_collection = []
        for name, attr in self._attributes.items():
            if name.lower() not in ["stitch"]:
                _attribute_collection.append(attr(name, self._db, self._parser))
        return _attribute_collection

    def _get_fabric_attrs(self):
        folder = self._naming.material_path.format(self._naming.matfolders[1], "")
        for f in os.listdir(folder):
            self._attributes[f] = FabricLogAttribute

class LogAttribute:
    def __init__(self, name="generic", db=None, parser=None) -> None:
        self.name = name
        self.value = None
        self._db = db
        self._parser=parser

    def get(self, attributes=None):
        return ""

class BgrAttribute(LogAttribute):
    def __init__(self, name="Background", db=None, parser=None) -> None:
        LogAttribute.__init__(self, name, db=db, parser=parser)
        self._content = {"d48791": "Bright",
                         "ebc5b0": "Azure",
                         "e6ad86": "Pink Sunset",
                         "f4bf86": "Orange Sunset",
                         "f5a685": "Pacific Island",
                         "f5a893": "Calm",
                         "f5b46e": "Restless",
                         "f6baaa": "Cream Cake",
                         "f9cf87": "Sunset",
                         "f298ad": "Magenta",
                         "f39183": "Lavender Aroma",
                         "ffc27f": "Sahara Sands",
        
        
        }

    def get(self, attributes):
        
        for k, v in attributes.items():
            if "bgr" in k.lower():
                return self._content[v]
        return "None"

class NftLogAttribute(LogAttribute):
    def __init__(self, name="Upcycled NFT", db=None, parser=None) -> None:
        LogAttribute.__init__(self, name, db=db, parser=parser)

    def get(self, attributes):
        
        for k, v in attributes.items():
            if "print_" in k.lower():
                return self._parser.get(v, "tag")
        return "None"

class NftAuthorLogAttribute(LogAttribute):
    def __init__(self, name="NFT Author", db=None, parser=None) -> None:
        LogAttribute.__init__(self, name, db=db, parser=parser)

    def _get_nft(self, attributes):
        for k, v in attributes.items():
            if "print_" in k.lower():
                return v
        return "None"

    def get(self, attributes):
        
        result = self._get_nft(attributes)
        if result!="None":
            return self._parser.get(result, "author")


    def get_old_(self, attributes):
        result = self._get_nft(attributes)
        path = TEXTURES + "/NFT"
        if result!="None":
            for folder in [x for x in os.listdir(path)]:  # if x.lower()!= "unknown"]:
                if os.path.isdir(path + "/" + folder):
                    if result.lower() in [x.split(".")[0].lower() for x in os.listdir(path + "/" + folder)]:
                        return folder
        return "None"

class PantiesModelLogAttribute(LogAttribute):
    def __init__(self, name="Identity", db=None, parser=None) -> None:
        LogAttribute.__init__(self, name, db=db, parser=parser)
        self._dict = PantiesModels()

    def get(self, attributes=None):
        model = bpy.data.filepath.split(".")[-2][-4]
        return self._dict.get(model)

class PartNumberLogAttribute(LogAttribute):
    def __init__(self, name="Parts", db=None, parser=None) -> None:
        LogAttribute.__init__(self, name, db=db)

    def get(self, attributes):
        return len([x for x in attributes if "stitch" not in x.lower()])

class FabricLogAttribute(LogAttribute):
    def __init__(self, name="Fabric", db=None, parser=None) -> None:
        LogAttribute.__init__(self, name, db=db, parser=parser)

    def get(self, attributes):
        _dict = {x.split("_")[0].lower(): self._db.get(x) for x in attributes.values() if "_" in x}
        try:
            return _dict[self.name.lower()]
        except KeyError as e:
            return "None"

    def _get_old(self, attributes):
        _dict = {x.split("_")[0].lower(): x.split("_")[1] for x in attributes.values() if "_" in x}
        try:
            return _dict[self.name.lower()]
        except KeyError as e:
            return "None"

class TrimLogAttribute(LogAttribute):
    def __init__(self, name="Trim", db=None, parser=None) -> None:
        LogAttribute.__init__(self, name, db=db)

    def get(self, attributes):
        return "Metal" in attributes.keys()
    
class PatchLogAttribute(LogAttribute):
    def __init__(self, name="Trim", db=None, parser=None) -> None:
        LogAttribute.__init__(self, name, db=db)

    def get(self, attributes):
        _result = [x for x in attributes.keys() if x.lower().startswith("patch")]
        if len(_result) == 1:
            return _result[0].split("_")[1]
        elif len(_result) > 1:
            return "Multiple"
        return "None"
    
class TextureLogReplacement:
    def __init__(self) -> None:
        self._content = pd.read_csv("assets/csv/material_tags.csv")
        self._working = self._content.columns[1]
        self._log = self._content.columns[2]  # 3 if Malcolm's version

    def get(self, key):
        return self._get(key)

    def _get(self, key):
        try:
            return self._content.loc[self._content[self._working]==key][self._log].iloc[0]
        except KeyError:
            # background
            return None
        except IndexError:
            # nft value
            return None