import os

folders = ["Terry", "Twill", "Weave", "Lace"]
path = "C:/Users/STFED/_A/_other/PantiesPorn/assets/Master_Generator/Material_Library/NonSubstance"
disp_folder = "Displacment"

for folder in folders:
    full_path = f'{path}/{folder}/{disp_folder}'
    for img in os.listdir(full_path):
        imgname = img.split(".")[-2]
        if not imgname.endswith("_D"):
            try:
                os.rename(f'{full_path}/{img}', f'{full_path}/{imgname}_D.png')
            except FileExistsError:
                pass