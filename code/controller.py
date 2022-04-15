import bpy
from condition import Condition
from materialdictionary import MaterialDictionary
from part import FabricPart
from weights import Weights


class Controller:
    def __init__(self) -> None:
        self.values = []
        self._dict = MaterialDictionary()
        self._condition = Condition()
        self._weights = Weights()
        
    def make(self, configuration):
        return self._make(configuration)

    def _make(self, configuration):
        self._control_textures(configuration)

    def _are_adjacent(self, part1, part2):
        try:
            if isinstance(part1, FabricPart) and isinstance(part2, FabricPart):
                front1, side1, *_ = part1.name.lower().split("_")
                front2, side2, *_ = part2.name.lower().split("_")
                return front1 == front2 or side1 == side2
        except Exception:
            return False

    def _check_fabric(self, part1, part2):
        if self._are_adjacent(part1, part2):
            values = part1.active_values + part2.active_values
            return len(values) == len(set(values))
        return True

    def _control_textures(self, configuration):
        for i, part in enumerate(configuration.parts[configuration.active_variant]):
            for j, part1 in enumerate(configuration.parts[configuration.active_variant]):
                if j > i:
                    if not self._check_fabric(part, part1):
                        print("EVALUATION: Active values", part.active_values)
                        print("EVALUATION: Active values", part1.active_values)
                        part1.make()
        # return configuration
