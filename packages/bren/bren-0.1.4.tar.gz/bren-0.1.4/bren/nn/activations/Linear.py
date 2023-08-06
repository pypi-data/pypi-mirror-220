from bren.nn.activations.Activation import Activation


def linear(x): return x


class Linear(Activation):
	"""
	The linear activation function perform no operation on the input

	Parameters
	----------
	x (`br.Variable`): The input Array
	name (`str`): The name of the activation.
	"""

	def __init__(self, name="linear", **kwargs) -> None:
		super().__init__(linear, name, **kwargs)