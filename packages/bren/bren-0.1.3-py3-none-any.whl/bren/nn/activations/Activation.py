from bren.nn.layers import Layer


class Activation(Layer):
	"""
	The `Activation` class is a child of the `Layer` class and is mainly used to produce custom activation funtions.

	Parameters
	__________
	func (`function`): the activation function
	name (`str`): the name of the `Activation` object
	"""

	def __init__(self, func=None, name=None, **kwargs) -> None:
		self.func = func
		super().__init__(name, **kwargs)
		self.set_built(True)
		self.__class__.__name__ = func.__name__

	def call(self, inp, training=None, **kwargs):
		return self.func(inp)
