from bren.nn.losses.Loss import Loss
from bren.nn.losses.MeanSquaredError import mse, mean_squared_error, MeanSquaredError, MSE
from bren.nn.losses.CatrgoricalCrossEntropy import categorical_cross_entropy, CategoricalCrossEntropy
from bren.nn.utils import AliasDict


__all__ = [Loss, MeanSquaredError, CategoricalCrossEntropy]

LOSSES = AliasDict()

for cls in __all__:
    LOSSES[cls.__name__] = cls

LOSSES.add(MeanSquaredError.__name__, "MSE", "mse", "mean_squared_error")
    
def get_loss(name):
	return LOSSES[name]