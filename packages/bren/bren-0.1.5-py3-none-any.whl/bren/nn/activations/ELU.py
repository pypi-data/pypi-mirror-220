import numpy as np
from bren.nn.activations.Activation import Activation
from bren.autodiff.operations.ops import custom_gradient


def elu_grad(a, alpha, dout, value):
	return [np.multiply(dout, np.where(a > 0, 1, alpha * np.exp(a)))]
@custom_gradient(elu_grad)
def elu(a, alpha): 
	return np.where(a > 0, a, alpha * (np.exp(a) - 1))


class ELU(Activation):
	"""
	Perform the ELU activation function on the input. 
	For input values greater than 1 the output will be linear (`x`), while negative values will be computed as `alpha * np.exp(x) - 1` with the alpha hyperparameter determining what negative value the function approches for more and more negative values of the inputs.

	Paratmeters
	-----------
	alpha (`float`): Hyperparameter which determines the negative value which the funcion approached for more and more negative value of x
	x (`br.Variable`): The input Array.
	name (`str`): The name of the activation.
	"""

	def __init__(self, alpha=1, name="elu", **kwargs) -> None:
		super().__init__(elu, name, **kwargs)
		self.alpha = alpha
		self.additional_args.append(self.alpha)
