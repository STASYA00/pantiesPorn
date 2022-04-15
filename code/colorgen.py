import numpy as np

class ColorGenerator:
    """
    Class that generates colors.
    """
    def __init__(self) -> None:
        """
        Class initialization.
        """
        self.name = ""

    def make(self):
        """
        Function that generates a random color in RGB space.
        returns: color, tuple (r, g, b), values range from 0 to 1
        """
        return self._make()

    def _make(self):
        """
        Function that generates a random color in RGB space.
        returns: color, tuple (r, g, b), values range from 0 to 1
        """
        _colors = []
        for _ in range(3):
            _colors.append(round(np.random.random(), 2))
        return Color(_colors)

class Color:
    """
    Class that represents a color.
    """
    def __init__(self, colors) -> None:
        self._spacer = "_"
        self.values = tuple(self._check(colors))
        self.name = self._name()

    def _check(self, value):
        if len(value) == 3:
            for v in value:
                assert v <= 255 and v>=0, "Wrong color value input, {}".format(v)
            return value

    def _name(self):
        return self._spacer.join([str(x) for x in self.values])