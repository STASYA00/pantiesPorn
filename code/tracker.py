import json
import os
import sys


from config import SCRIPT_PATH
sys.path.append(SCRIPT_PATH)

from treelib import Tree

from colorgen import Color
from naming import NamingProtocol
from part import SubstancePart


class Tracker:
    def __init__(self, configuration) -> None:
        self.tree = Tree()
        self.parent = "root"
        self._naming = NamingProtocol()
        self._content = {}
        self._setup()
        self._structure = self._make_structure(configuration)
        self._hidden_value = "hidden"

    def export(self, filename="result"):
        return self._export(filename)

    def make(self, configuration):
        return self._make(configuration)

    def get(self, ind=-1):
        if ind < 0:
            ind = len(list(self._content.keys())) - 1
        return self._content[ind]

    def _add(self, configuration):
        new_index = 0
        indices = list(self._content.keys())
        if len(indices) > 0:
            new_index = max(indices) + 1
        self._content[new_index] = {}
        for key in self._structure:
            self._content[new_index][key] = self._get_value(configuration, key)

    def _build(self, configuration) -> bool:
        _prev_node = self.parent
        for level, material in enumerate(self._structure):
            value = self._get_value(configuration, material)
            _prev_node = self._build_node(level, value, _prev_node)
            
        return True

    def _build_node(self, level, value, parent):
        _id = str(level) + "_" + value
        if not _id in list(self.tree.nodes.keys()):
            self.tree.create_node(value, _id, parent=parent)
        return _id

    def _export(self, filename):
        # _js = self.tree.to_dict()
        _js = self._content
        filename = self._naming.json_name.format(filename)
        with open(filename, "w") as f:
            f.write(json.dumps(_js, indent=4))

    def _get_value(self, configuration, material):
        _print = 0
        if material.startswith("print") and material.lower()!="print_loop":
            _print = 1
        part = configuration.get_part(material)
        if len(part.active_values) > _print:
            return part.active_values[_print].split(".")[0]
        return self._hidden_value

    def _is_child(self, parent, child):
        """
        Function that checks whether a node already exists from this parent on this level.
        :param: parent          parent node identifier, str
        :param: child           child node identifier, str

        return: result          evaluation result, bool
        """
        # TODO: check if parent exists in nodes
        return child in self.tree[parent].successors(self.tree.identifier)

    def _in_tree(self, configuration):
        """
        Function that checks whether a configuration already exists in the tree.
        :param: configuration           model configuration, Panties
        return: result                  evaluation result, bool
        """
        # TODO: add _id to naming class
        _prev_node = self.parent
        for level, material in enumerate(self._structure):
            part = configuration.get_part(material)
            if not part.active_values:
                return False
            _id = str(level) + "_" + part.active_values[0]
            if not self._is_child(_prev_node, _id):
                return False
            _prev_node = _id
        return True

    def _is_color_material(self, part):
        for m in part.materials:
            if m.colorgen:
                return True

    def _make(self, configuration):
        """
        Function that checks whether a configuration exists; if it doesn't a new
        configuration is added to the tree.
        :param: configuration           model configuration, Panties
        return: result                  evaluation result, bool
        """
        self._structure = self._make_structure(configuration)
        self._add(configuration)
        if not self._in_tree(configuration):
            return self._build(configuration)

    def _setup(self):
        self.tree.create_node(self.parent, self.parent)

    def _make_structure(self, configuration) -> list:
        _structure = []
        for part in configuration.parts[configuration.active_variant]:
            if not isinstance(part.materials[0], SubstancePart):
                if self._is_color_material(part):
                    _structure.append(part.mesh.active_material.name)
                else:
                    _structure = [part.mesh.active_material.name] + _structure
                if len(part.active_values) > 1:
                    _structure = ["print_" + part.mesh.active_material.name] + _structure
        return _structure