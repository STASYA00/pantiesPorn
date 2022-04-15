class Weights:
    def __init__(self) -> None:
        self.default = 0.5
        self.content = {"trim": 0.5,
                        "nft": 0.90,  # 0.15
                        "lace": 0.2,
                        "lace_nft": 0.9
        }

    def get(self, key):
        if key in list(self.content.keys()):
            return self.content[key]
        else:
            return self.default