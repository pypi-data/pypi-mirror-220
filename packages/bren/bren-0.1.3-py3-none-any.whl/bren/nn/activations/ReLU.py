import numpy as np
from bren.nn.layers.Layer import Layer
from bren.autodiff.operations.ops import custom_gradient


def relu_grad(a, leak, dout, value): 
	return [np.multiply(dout, a > 0)]
@custom_gradient(relu_grad)
def relu(a, leak): return np.maximum(a * leak, a)


class ReLU(Layer):
	"""
	[NOTE]: This is also the leaky ReLU function, change the leak parameter to change to leaky ReLU. By default the `leak` parameter for this function is 0 to simulate the nature of a regular ReLU function.

	Performs the ReLU activation function on the inputs.
	For positive values the output is linear (`x`) while for negative values the output is `x * leak` where leak is the gradient of the straight line for values smaller than 0. 

	Parameters
	----------
	leak (`float`): the gradient of the straight lines for values smaller than 0
	x (`br.Variable`): The input Array
	name (`str`): The name of the activation.
	"""

	def __init__(self, leak=0, name=None, **kwargs) -> None:
		self.leak = leak
		super().__init__(name, **kwargs)

	def call(self, x): return relu(x, self.leak)