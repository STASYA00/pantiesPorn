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
            _colors.append(np.random.random())
        return tuple(_colors)