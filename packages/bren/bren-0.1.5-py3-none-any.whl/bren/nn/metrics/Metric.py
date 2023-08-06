from bren import Variable
import numpy as np


class Metric(object):
	"""
	The base `Metric` class
	"""

	def __init__(self) -> None: 
		self.__reset = np.vectorize(self.__reset, cache=False)
		self.variables = []

	def __reset(self, var): var.assign(0) 

	def update(self, y_pred, y_true, weights=None):
		"""
		The `update` function is called at the end of every pass through of training data.

		Parameters
		----------
		y_pred (br.Variable): the predicted values from the model
		y_true (br.Variable): the actual values
		"""
		...

	def reset(self):
		"""
		Resets all of the local Variables.
		"""
		self.__reset(self.variables)

	def add_weight(self, val, **kwargs):
		"""
		Creates a new Variable.

		Parameter
		---------
		val (`list`, `np.ndarray`): The value of the Variable. 
		"""
		var = Variable(val, **kwargs)
		self.variables.append(var)
		return var
	
	def result(self):
		"""
		Returns the final current value of the metrics
		"""
		...

	def __call__(self, y_pred, y_true, **kwargs): 
		self.update(y_pred, y_true)
		return self.result(**kwargs)

