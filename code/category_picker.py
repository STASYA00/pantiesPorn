import numpy as np
from condition import Condition
from materialdictionary import MaterialDictionary
from weights import Weights


class CategoryPicker:
    def __init__(self) -> None:
        
        self._dict = MaterialDictionary()
        self._condition = Condition()
        self._weights = Weights()

    def make(self, part):
        return self._make(part)

    def make_special(self, part):
        category = self._dict.get(part.mesh.active_material.name.lower())
        values = [True for x in part.materials]
        return category, values

    def _make(self, part):
        # if lace          - nonNFT material, check for print, otherwise color
        # if other - print - nonNFT material, unstack print node
        # if other + print - NFT material (substance)

        category = "random"
        has_lace = self._satisfies("lace", part.name)
        #has_print = self._satisfies("print", part)
        has_print = part.has_print
        if has_lace:
            has_print = self._satisfies("nft_lace", part.name)
        

        if has_print and not has_lace:
            # Substance material with print
            values = [True, False]
            category = "NFT_base"
        else:
            # nonSubstance material
            values = [False, True]
            if has_lace:
                category = "lace"
            else:
                category = self._dict.get("random", exception=["lace"])
        values = [True]  # we dont have substance materials anymore
        return category, values

    def _check_condition(self, condition, partname):
        func = self._condition.get(condition)
        if func:
            return func(partname)
        return True  # no condition regarding this => satisfies

    def _check_weights(self, condition):
        return np.random.random() < self._weights.get(condition)


    def _satisfies(self, condition, partname):
        if self._check_condition(condition, partname):
            return self._check_weights(condition)
        return False
