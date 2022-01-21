import bpy
import sys

# from config import SCRIPT_PATH

# sys.path.append(SCRIPT_PATH)

import numpy as np

def deselect_all():
	"""
	Function that deselects all the objects in the scene.
	:return: None
	"""
	for obj in bpy.data.objects:
		obj.select_set(False)

def get_nodes_link(node1, node2, links):
	for link in [x for x in links]:
		if node1.name == link.from_node.name:
			if node2.name == link.to_node.name:
				return link

def normalize_prob(prob):
    return np.array(prob) / np.array(prob).sum(0)

def select(_volume):
	_volume.select_set(True)
	bpy.context.view_layer.objects.active = _volume