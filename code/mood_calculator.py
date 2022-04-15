import numpy as np

class MoodCalculator:
    def __init__(self) -> None:
        self.value = 0.8

    def make(self, configuration):
        return self._make(configuration)

    def _get_mood(self, value):

        # ideally partially in naming protocol
        if "_" in value:
            try:
                return value.split("_")[1]
            except Exception as e:
                print("Failed to get the mood of {}".format(value))
                print(repr(e))
        return ""

    def _make(self, configuration):
        _values = []
        for part in configuration.parts[configuration.active_variant]:
            for val in part.active_values:
                _values.append(self._get_mood(val))
        _values = [x for x in _values if x]
        if _values:
            counts = np.unique(_values, return_counts=True)[1]
            return np.sum((counts / np.sum(counts)) < self.value), self._most_freq(_values)
        else:
            return True, "None"

    def _most_freq(self, values):
        if len(values) > 0:
            v, c = np.unique(values, return_counts=True)
            return v[np.where(c==np.max(c))[0][0]]