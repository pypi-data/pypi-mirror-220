from bren.nn.layers import Layer
import numpy as np
from bren.autodiff.operations.ops import custom_gradient


class Softmax(Layer):
    """
    Returns a Array of values of the same size as its inputs where `tmp = np.exp(x)` and `tmp / np.sum(tmp)` is returned.

    Parameters
    ----------
    name (`str`): The name of the Layer.
    """

    def __init__(self, name=None, **kwargs) -> None:
        super().__init__(name, **kwargs)

    def call(self, x):
        tmp = np.exp(x)
        return tmp / np.sum(tmp)