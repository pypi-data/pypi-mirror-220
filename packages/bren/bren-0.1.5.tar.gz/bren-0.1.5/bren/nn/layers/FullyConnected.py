from bren.nn.layers import Layer
from bren.nn.initialisers import get_initialiser, Initialiser, initialiser_from_func
from bren.nn.activations import get_activation, Activation
from bren.nn.utils import rename_key


def set_activation(activation, custom_obs={}):
	out = None

	if type(activation) == str or activation is None: 
		try: out = get_activation(activation)()
		except KeyError:
			try: out = set_activation(custom_obs[activation])
			except KeyError:
				raise KeyError(f"custom object {activation} cannot be found") 
			
	elif issubclass(type(activation), Layer):
		out = activation
	elif type(activation).__name__ == "function":
		out = Activation(activation, name=activation.__name__)
	else: raise AttributeError(f"{activation} is of invalid type for activation")

	return out

def set_initialiser(initialiser):
	out = None

	if type(initialiser) == str:
		out = get_initialiser(initialiser)
	elif issubclass(type(initialiser), Initialiser):
		out = initialiser 
	elif type(initialiser).__name__ == "function":
		out = initialiser_from_func(initialiser)
	else: raise AttributeError(f"{initialiser} is of invalid type for initialisers")

	return out
	

class FullyConnected(Layer):

	"""
	The `FullyConnected` layer returns a layer with a specified amount of `units` where each unit is conceptually connected to every other unit in the previous layer.

	Parameters
	----------
	units (`int`): The number of units for the layer.
	activation (`str`, `Activation`, `function`): the activation function for the layer. After the weights and biases have been applied to the inputs, the result will then be passed through the specified activation function. By default, this is set to `None` which is equivalent to the `Linear` activation function.
	weights	 
	weights_initialiser (`str`, `Initialiser`, `function`): The initialiser function of the weights.
	bias_initialiser (`str`, `Initialiser`, `function`): The initialiser function of the biases.
	use_bias (`bool`): Determines the inclusion of the bias.
	name ("str"): the name of the `FullyConnected` Layer.
	"""

	def __init__(self, units, 
						activation=None, 
						weights_initialiser="GlorotUniform", 
						bias_initialiser="GlorotUniform", 
						use_bias=True, 
						name=None, **kwargs) -> None:
		super().__init__(name, **kwargs)

		self._units = units
		self.activation = set_activation(activation, self.custom_objs)

		self.weights_initialiser = set_initialiser(weights_initialiser)
		self.bias_initialiser = set_initialiser(bias_initialiser)

		self.use_bias = use_bias

	@property
	def units(self): return self._units
	@units.setter
	def units(self, value): ...

	def build(self, input_shape, input_dtype, **kwargs):
		self.weights = self.add_weight(
			self.weights_initialiser(shape=(self.units, input_shape[0]))(), dtype=input_dtype) 

		self.bias = self.add_weight(
			self.bias_initialiser(shape=(self.units, 1))() if self.use_bias else 0, dtype=input_dtype)

		return super().build(input_shape, input_dtype, **kwargs)

	def call(self, x):
		output = (self.weights @ x) + self.bias
		
		return self.activation(output)
	
	def config(self):
		self.set_config(rename_key(super().config(), "_units", "units"))
		self.__dict__["bias_initialiser"] = self.bias_initialiser.__name__
		self.__dict__["weights_initialiser"] = self.weights_initialiser.__name__
		self.__dict__["activation"] = self.activation.__class__.__name__
		return self.__dict__

# aliases
FC = FullyConnected
Dense = FullyConnected