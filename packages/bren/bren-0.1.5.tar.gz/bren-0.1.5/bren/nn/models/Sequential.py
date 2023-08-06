from bren.nn.models import Model
import numpy as np
import bren as br


class Sequential(Model):
    """
    The `Sequential` model takes in a list of layers and passes the data through each of the layers consecutively.

    Parameters 
    ----------
    layers (`list`): The list of layers.
    """

    def __init__(self, layers, **kwargs) -> None:
        super().__init__(**kwargs)
        self.layers = layers

    def build(self, input):
        super().build(input)
        
        for layer in self.layers:
            self.add_weight(layer.trainable)

    def call(self, x, training=None):
        Z = x
        for layer in self.layers:
            Z = layer(Z, training=training)
        return Z
    
    def serialise(self):
        for i, layer in enumerate(self.layers):
            self.layers[i] = layer.config()
        return super().serialise()
    
    def save(self, filepath):
        return super().save(filepath)