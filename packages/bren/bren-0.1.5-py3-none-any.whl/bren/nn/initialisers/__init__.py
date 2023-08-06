from bren.nn.initialisers.Initialiser import Initialiser, initialiser_from_func
from bren.nn.initialisers.GlorotNormal import GlorotNormal
from bren.nn.initialisers.GlorotUniform import GlorotUniform
from bren.nn.initialisers.HeNormal import HeNormal
from bren.nn.initialisers.HeUniform import HeUniform
from bren.nn.utils import AliasDict


__all__ = [Initialiser, GlorotNormal, GlorotUniform, HeNormal, HeUniform, initialiser_from_func]


INITIALISERS = AliasDict({})

for cls in __all__:
	INITIALISERS[cls.__name__] = cls

INITIALISERS.add(GlorotNormal.__name__, "glorot_normal", "glorotnormal")
INITIALISERS.add(GlorotUniform.__name__, "glorot_uniform", "glorotuniform")
INITIALISERS.add(HeNormal.__name__, "he_normal", "henormal")
INITIALISERS.add(HeUniform.__name__, "he_uniform", "heuniform")

def get_initialiser(name): return INITIALISERS.get(name, name)