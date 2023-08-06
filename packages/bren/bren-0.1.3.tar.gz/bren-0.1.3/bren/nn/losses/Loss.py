from bren.nn.metrics import Metric
import numpy as np

class Loss(Metric):
	"""
	The base `Loss` class

	Parameters
	----------
	name (`str`): The name of the function.
	"""

	def __init__(self, name=None, **kwargs) -> None: 
		self.func = kwargs.get("func", None)
		self.name = name or self.__class__.__name__

	def __call__(self, y_pred, y_true, *args, **kwargs): 
		out = self.func(y_pred, y_true, *args, **kwargs)
		return np.sum(out)
		