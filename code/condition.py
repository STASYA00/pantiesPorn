class Condition:
    def __init__(self) -> None:
        self.content = {"print": self._print,
                        "lace": self._lace,
        }

    def get(self, key):
        if key in list(self.content.keys()):
            return self.content[key]
        return False

    def _print(self, mesh_name):
        return "front" in mesh_name.lower() and "patch" not in mesh_name.lower()

    def _lace(self, mesh_name):
        #return "back" in mesh_name.lower()
        return True

