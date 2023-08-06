import numpy as np


class Optimiser(object):
	"""
	The base `Optimiser` class.
	"""

	def __init__(self) -> None: 
		self.update = np.vectorize(self.update, cache=True, otypes=[list])

	def apply_gradients(self, vars, grads, **kwargs): 
		"""
		Updates the given variables with the given gradients of the variables with respect to the loss, calculated by autodiff.

		Parameter
		---------
		vars (`list`): A list of the trainable Variables.
		grads (`list`): A list of the respective Gradients.

		"""
		...

	def update(*args, **kwargs): 
		"""
		A vectorised function which performs the updating of the value of the variables (called within the `apply_gradients` function).
		"""
		...