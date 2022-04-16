# To run the code:
# $ blender -b assets/models/MP_04_01.blend --python code/run.py
import argparse
import os
import sys
import textwrap
from time import time

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from config import RENDERS
from pipeline import RenderPipeline, MainPipeline

if __name__=="__main__":
    args = None
    if '--' in sys.argv:
        argv = sys.argv[sys.argv.index('--') + 1:]
        parser = argparse.ArgumentParser(
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description=textwrap.dedent('''\
		USAGE: blender -b assets/Master_Generator/MP_10/MP_10_01.blend --python code/run.py 
        -- -start 0 -frames 10 -output Renderings

		------------------------------------------------------------------------

		This is an algorithm that generates different texture combinations of a
        model of panties given to Blender. The textures are taken from the 
        folder defined in the config file.

		------------------------------------------------------------------------

		'''), epilog=textwrap.dedent('''\
		The algorithm will be updated with the changes made in the strategy.
		'''))
        parser.add_argument('start',type=int,help='frame the generation starts with, int',
                            default=0)
        parser.add_argument('frames',type=int,help='number of frames to generate for \
                                                    this model',
                            default=10)
        parser.add_argument('output',type=str,help='output folder to save images to',
                            default='Renderings')
        args = parser.parse_known_args(argv)[0]
        try:
            args=parser.parse_args()
        except SystemExit as e:
            print("")
    if args:
        OUTPUT_FOLDER = args.output
        RENDERS = args.frames
        START = args.start
    else:
        START = 0
    print(START, RENDERS)
    t1 = time()
    pipe = MainPipeline(RENDERS)
    pipe.run(START)
    print(time() - t1)



# file 02
# change bgr material name
# change back_lace mesh names x3
# lights to light
# lamp names