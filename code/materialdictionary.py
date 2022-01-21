class MaterialDictionary:
    def __init__(self) -> None:
        self.content = {"lace": "LACES",
                        "tartan": "TARTAN",
                        "terry": "TERRY",
                        "random": "RANDOM",
                        "bgr": "Background"
                        }

    def get(self, fabric):
        assert fabric.lower() in [x.lower() for x in self.content.keys()], "Fabric type {} is not implemented".format(fabric)
        return self.content[fabric]