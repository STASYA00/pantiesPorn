import numpy as np

class MaterialDictionary:
    def __init__(self) -> None:
        # restructure EVERYTHING
        self.default = "random"
        self.content = {"substance": {
                            "lace_back": "Lace_Square",
                            "lace_trim": "Lace_Trim",
                            "bgr": "Background",
                            "loop": "Loop",
                            "NFT_base": "NFT_Base",
                            "print": "NFT",
                            "ribbon": "Lace_Ribbon",
                            "rope": "Loop",
                            "silk": "Metallic_Silk",
                            "zipper": "Zipper",
                            },
                        "nonsubstance": {
                                         #"fuzz": "Fuzz",
                                         "lace": "Lace",
                                         "terry": "Terry",
                                         "twill": "Twill",
                                         "weave": "Weave",
                                         },
                        
                        }
        self.special = {"dominant_01": ("Weave", "Weave_Pink_02.jpg"),
                        "dominant_02": ("Weave", "Weave_Orange_03.jpg"),
                        "dominant_03": ("Weave", "Weave_Orange_01.jpg"),
                        "key": ("Metal", "slnndb2c_4K_Roughness.jpg"),
                        "chain": ("Metal", "sewlddcc_4K_Roughness.jpg"),
                        "badge": ("Metal", "slnndb2c_4K_Roughness.jpg")
        }

    def get(self, fabric, exception=[]):
        if fabric.lower() in list(self.special.keys()):
            return self.get_special[fabric.lower()]
        if fabric.lower() == self.default:
            return self._get_random(exception)
        for value in list(self.content.values()):
            if self._check_fabric(fabric, value):              
                return self._get_fabric(fabric, value)
        print("Fabric type {} not implemented".format(fabric))
        raise AssertionError

    def get_special(self, fabric) -> tuple:
        if fabric.lower() in list(self.special.keys()):
            return self.special[fabric.lower()]
        for key in self.special.keys():
            if key in fabric.lower():
                return self.special[key][1]


    def _get_random(self, exception=[]):
        _options = list(set(self.content["nonsubstance"].keys()) - set(exception))
        _options = [self.content["nonsubstance"][x] for x in _options]
        return np.random.choice(_options, 1)[0]

    def _check_fabric(self, fabric, value):
        #print([x.lower() for x in value.keys() if fabric.lower() in x.lower()])
        return fabric.lower() == self.default.lower() or \
            len([x.lower() for x in value.keys() if fabric.lower().startswith(x.lower())]) > 0

    def _get_fabric(self, fabric, value):
        return value[[x.lower() for x in value.keys() if fabric.lower().startswith(x.lower())][0]]


class SubstanceDictionary:
    def __init__(self) -> None:
        # node_name : (socket_name, string in imagefile)
        self.content = {"Mix": [("Color1", "BaseColor"), 
                                ("Color2", "print")],
                        'Hue Saturation Value': [("Color", "BaseColor")],
                        "Principled BSDF": [("Base Color", "BaseColor"),
                                            ("Alpha", "Alpha"),
                                            ("Metallic", "Metallic"),
                                            ("Roughness", "Roughness")],
                        "Displacement": [("Height", "Displacement")],
                        "Normal map": [("Color", "Normal")],
                       }