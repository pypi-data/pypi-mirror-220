from bren.nn.metrics.Metric import Metric
from bren.nn.metrics.Accuracy import Accuracy
from bren.nn.metrics.MeanSquaredError import MeanSquaredError
from bren.nn.metrics.CategoricalCrossEntropy import CategoricalCrossEntropy
from bren.nn.utils import AliasDict
import numpy as np


__all__ = [Metric, Accuracy, MeanSquaredError, CategoricalCrossEntropy]


METRICS = AliasDict()

for cls in __all__:
    METRICS[cls.__name__] = cls
    
METRICS.add(Accuracy.__name__, "accuracy")
METRICS.add(MeanSquaredError.__name__, "mse", "mean_squared_error", "MSE")
METRICS.add(CategoricalCrossEntropy.__name__, "categorical_cross_entropy")


def get_metric(name):
	return METRICS[name]


def metric_from_loss(func, name=None):
	class MetricFromLoss(Metric):
		def __init__(self) -> None:
			super().__init__()
			self.__class__.__name__ = name or func.__name__
			self.total = self.add_weight(0)
			self.count = self.add_weight(0)

		def update(self, y_pred, y_true, weights=None):
			self.total.assign_add(func(y_pred, y_true))
			self.count.assign_add(1)
		
		def result(self):
			return np.sum(self.total / self.count)

	return MetricFromLoss
		