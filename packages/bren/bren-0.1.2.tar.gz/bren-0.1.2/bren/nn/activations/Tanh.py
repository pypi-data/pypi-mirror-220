import numpy as np
from bren.nn.layers.Layer import Layer


def tanh(x): return np.tanh(x)

class Tanh(Layer):

	"""
	Performs `np.tanh(x)` on the inputs

	Parameters
	----------
	x (`br.Variable`): The input Array
	name (`str`): The name of the activation.	
	"""

	def __init__(self, name=None, **kwargs) -> None:
		super().__init__(name, **kwargs)

	def call(self, x): return tanh(x)