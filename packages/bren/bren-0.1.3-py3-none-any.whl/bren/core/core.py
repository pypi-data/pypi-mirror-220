import numpy as np
from bren.autodiff.nodes import Var, Const
from bren.core.Array import Array


class Variable(Array):
	"""
	Produces a `Variable` object (wrapped numpy array) which keeps track of functions which were performed on it.

	Parameters: 
	-----------
	value (`np.ndarray`, `list`): Value to be stored by the object
	dtype (`str`): The data type of the array
	name (`str`): The name of the array
	"""
	def __init__(self, value, dtype="float32", name=None, **kwargs) -> None:
		super().__init__(value, dtype, name, **kwargs)
		self._source = kwargs.get("source") or Var(self._i, name=self.name)


class Constant(Array):
	"""
	Produces a `Constant` object (wrapped numpy array) which does not have a gradient.

	Parameters: 
	-----------
	value (`np.ndarray`, `list`): Value to be stored by the object
	dtype (`str`): The data type of the array
	name (`str`): The name of the array
	"""

	def __init__(self, value, dtype="float32", name=None, **kwargs) -> None:
		super().__init__(value, dtype, name, **kwargs)
		self._source = kwargs.get("source") or Const(self._i, name=self.name)
