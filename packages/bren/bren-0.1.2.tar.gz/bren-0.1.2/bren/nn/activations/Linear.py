from bren.nn.layers.Layer import Layer


class Linear(Layer):
	"""
	The linear activation function perform no operation on the input

	Parameters
	----------
	x (`br.Variable`): The input Array
	name (`str`): The name of the activation.
	"""

	def __init__(self, name=None, **kwargs) -> None:
		super().__init__(name, **kwargs)

	def call(self, x): return x
