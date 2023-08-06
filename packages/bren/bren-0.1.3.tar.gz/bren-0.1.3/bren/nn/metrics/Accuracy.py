from bren.nn.metrics import Metric
import numpy as np


class Accuracy(Metric):
	"""
	`Accuracy` calculates how amount of times which `y_pred` is equal to `y_true` with a given `leniency` and adds it to the variable `total`. When the result function is called, `total/count` is returned.
	
	Parameters
	----------
	precision (`int`): the decimal place at which `y_pred` is rounded before begin compared to `y_true`. They higher the precision, the more accurate `y_pred` will need to be to `y_true` to get a high accuracy.
	"""

	def __init__(self, precision=2) -> None:
		super().__init__()
		self.total = self.add_weight(0)
		self.count = self.add_weight(0)
		self.precision = precision

	def update(self, y_pred, y_true, weights=None, **kwargs):
		acc = np.sum(y_true == np.round(y_pred, decimals=self.precision)) / len(y_true)
		self.total.assign_add(acc)
		self.count.assign_add(1)

	def result(self):
		return self.total / self.count