from config import TEXTURES

class NamingProtocol:
    def __init__(self) -> None:
        
        self.filename = "output/{}_{}.png"  # 0001_categoryoption1_categoryoption2_...png
        self.blender_filename = "models/{}.blend"  # 0001.blend
        self.material_path = TEXTURES + "/{}/{}"  # type/image