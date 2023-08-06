from bren.nn.initialisers import Initialiser
import numpy as np


class GlorotNormal(Initialiser):
	"""
	Returns values taken from a normal distribution with mean 0 and a stddev of `sqrt(2 / (fan_in + fan_out))` where `fan_in` is a the number of inputs while `fan_out` is the number of outputs
	"""

	def __init__(self, shape, dtype="float32", **kwargs) -> None:
		super().__init__(shape, dtype, **kwargs)

		self.mean = kwargs.get("mean") or 0
		self.fan_in, self.fan_out = kwargs.get("inout") or shape
		fan_avg = (self.fan_in + self.fan_out) / 2
		self.stddev = np.sqrt(1 / fan_avg)

	def call(self, *args, **kwargs):
		return np.random.normal(self.mean, self.stddev, size=self.shape)
