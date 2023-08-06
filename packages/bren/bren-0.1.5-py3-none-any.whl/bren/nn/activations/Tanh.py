import numpy as np
from bren.nn.activations.Activation import Activation


def tanh(x): return np.tanh(x)

class Tanh(Activation):

	"""
	Performs `np.tanh(x)` on the inputs

	Parameters
	----------
	x (`br.Variable`): The input Array
	name (`str`): The name of the activation.	
	"""

	def __init__(self, name="tanh", **kwargs) -> None:
		super().__init__(tanh, name, **kwargs)
