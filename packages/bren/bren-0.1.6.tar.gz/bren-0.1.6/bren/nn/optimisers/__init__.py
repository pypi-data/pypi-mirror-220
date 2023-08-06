from bren.nn.optimisers.Optimiser import Optimiser
from bren.nn.optimisers.SGD import SGD
from bren.nn.optimisers.AdaGrad import AdaGrad
from bren.nn.optimisers.RMSProp import RMSProp
from bren.nn.optimisers.Adam import Adam
from bren.nn.utils import AliasDict


__all__ = [Optimiser, SGD, AdaGrad, RMSProp, Adam]


OPTIMISERS = AliasDict()

for cls in __all__:
    OPTIMISERS[cls.__name__] = cls

OPTIMISERS.add("AdaGrad", "adagrad")
OPTIMISERS.add("Adam", "adam")
OPTIMISERS.add("SGD", "sgd", "StochasticGradientDescent", "stochastic_gradient_descent")
OPTIMISERS.add("RMSProp", "rmsprop", "RootMeanSquaredPropogation", "root_mean_squared_propogation")

def get_optimiser(name):
    return OPTIMISERS[name]