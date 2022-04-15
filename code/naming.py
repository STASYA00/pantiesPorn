
from config import DISPLACEMENT_FOLDER, TEXTURES, OUTPUT_FOLDER

class NamingProtocol:
    def __init__(self) -> None:
        
        self.filename = OUTPUT_FOLDER + "/{}.png"  # 0001_categoryoption1_categoryoption2_...png
        self.blender_filename = "models/{}.blend"  # 0001.blend
        self.displacement = TEXTURES + "/{}/" + DISPLACEMENT_FOLDER
        self.material_path = TEXTURES + "/{}/{}"  # type/category/image
        self.json_name = OUTPUT_FOLDER + "/{}.json"
        self.matfolders = {0: "Substance", 1: "NonSubstance", 2: "NFT"}
        self.trim = TEXTURES + "/Chain"