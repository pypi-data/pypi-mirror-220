from bren.nn.metrics import Metric
import numpy as np


class MeanSquaredError(Metric):
	"""
	The metric equivalent of the `MeanSquaredError` loss function which computes the loss as `loss=mean((y_pred - y_true) ** 2)`
	"""

	def __init__(self) -> None:
		super().__init__()
		self.total = self.add_weight(0)
		self.count = self.add_weight(0)
		
	def update(self, y_pred, y_true, weights=None, **kwargs): 
		self.total.assign_add(kwargs.get("loss", np.sum((y_true - y_pred) ** 2))) 
		self.count.assign_add(1)

	def result(self): return self.total / self.count
