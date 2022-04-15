# rewrite as json for security reasons
# Tweakable parameters

# Output parameters
OUTPUT_FOLDER = "output_Lyzzo"  # where to save the rendered images
IMAGE_SIZE = (2000, 2000)  # resolution of the output images (width, height)
RENDERS = 5  # number of images to render
ASSEMBLE_FRAME = 1  # model configuration to assemble
ENGINE = 'CYCLES'  # engine to render in Blender. Can be CYCLES or EEVEE
SAMPLES = 64  # number of samples

# Excel file

# Scene specific
BGR_NAME = "Background"  # name of the background mesh object
PART_COLLECTION = "Patterns"
TEXTURES = "assets/Master_Generator/Material_Library"
DISPLACEMENT_FOLDER = "Displacment"
MESH_NAME = "MP"
LIGHT_SETUP = "Light"
TRIM_COLLECTION = "Trim"
CAMERA = "Gimball"

# Bureaucratic parameters
FACES = "sample/02-Texturing/TEST"  # path to the folder with the face textures
BLEND_DIR = "blend"  # path to save the .blend files (currently not in use)
MODEL_DIR = "models"  # path to save the .obj files (currently not in use)
JSON = "json"  # path to store generated json files
LOG = "json/log.json"  # filepath to log the generated configurations

SCRIPT_PATH = open('C:/Users/STFED/_A/_other/pantiesPorn/code/setup.txt').read()[:-1]  # path to the python packages

# Renamed Arm into Arms

# 200x200   5 frames -> 267 (4 min)
#          10 frames -> 580 (9 min)
# 1000x1000 5 frames -> 388 (6 min)

# 50 frames