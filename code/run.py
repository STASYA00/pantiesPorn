# To run the code:
# $ blender -b assets/MP10/MP10_03_02.blend --python code/run.py

import os
import sys
from time import time

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from config import RENDERS
from pipeline import RenderPipeline, MainPipeline

if __name__=="__main__":
    t1 = time()
    pipe = MainPipeline(RENDERS)
    pipe.run()
    print(time() - t1)