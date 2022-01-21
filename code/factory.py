from part import Part, FurPart, StitchPart

class Factory:
    def __init__(self) -> None:
        self.map = {"default": Part,
                    "hem": FurPart,
                    "parameteric": StitchPart       
        }

    def produce(self, name):
        for key, value in self.map.items():
            
            if key in name.lower():
                return value(name)
        return self.map["default"](name)