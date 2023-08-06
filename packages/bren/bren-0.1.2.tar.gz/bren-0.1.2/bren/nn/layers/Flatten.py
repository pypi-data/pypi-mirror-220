from bren.nn.layers import Layer
import numpy as np


class Flatten(Layer):
    """
    The `Flatten` Layer flattens (reduces the number of the dimensions of the array to 1) the input Array.

    Parameters
    ----------
    name (`str`): The name of the layer.
    """

    def __init__(self, name=None, **kwargs) -> None:
        super().__init__(name, **kwargs)

    def call(self, x):
        return x.flatten()[..., np.newaxis]
    

