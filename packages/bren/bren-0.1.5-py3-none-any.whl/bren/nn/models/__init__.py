from bren.nn.models.Model import Model
from bren.nn.models.Sequential import Sequential
from bren.nn.utils import AliasDict
from bren.nn.layers import __all__ as layers
import pickle

__all__ = [Model, Sequential]

MODELS = AliasDict({})


def get_model(name): return MODELS[name]


def deserialise_sequential_layers(model, custom_objects):
    OBJECTS = {**custom_objects}
    for layer in layers: OBJECTS[layer.__name__] = layer

    model_layers = model.layers
    
    for i, layer in enumerate(model.layers):
        L = OBJECTS[layer["layer"]](**layer, custom_obs=custom_objects, params=layer.get("trainable", []))
        model_layers[i] = L
        model_layers[i].set_built(True)
        try: model_layers[i].activation.set_built(True)
        except AttributeError: pass 
        model_layers[i].__dict__ = {**model_layers[i].__dict__, **layer["trainable"]} 


def load_model(filepath, custom_objects={}):
    with open(filepath, "rb") as f:
        model = pickle.load(f)

    model.set_custom_object(custom_objects)

    if model.__class__.__name__ == "Sequential":
        deserialise_sequential_layers(model, custom_objects)

    model.assemble(**model.config)
    
    return model


for cls in __all__:
    MODELS[cls.__name__] = cls