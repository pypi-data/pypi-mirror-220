from bren.nn.metrics import Metric
import numpy as np


class CategoricalCrossEntropy(Metric):
    """
    The metric equivalient of the `CategoricalCrossEntropy` loss function which computes the loss for multiclass classification, with `loss=-(sum(y_true * log(y_pred)))`
    """

    def __init__(self) -> None:
        super().__init__()
        self.total = self.add_weight(0)
        self.count = self.add_weight(0)
    
    def update(self, y_pred, y_true, weights=None, **kwargs):
        self.total.assign_add(kwargs.get("loss", -(np.sum(y_true * np.log(y_pred + 10e-10)))))
        self.count.assign_add(1)

    def result(self):
        return self.total / self.count