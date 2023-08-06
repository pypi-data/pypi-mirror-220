import numpy as np
from bren.nn.initialisers.Initialiser import Initialiser


class GlorotUniform(Initialiser):
	"""
	Returns values taken from a uniform distribution with endpoints `r` and `-r` where `r = (6 / fan_in + fan_out)` with `fan_in` being the number of inputs while `fan_out` being the number of outputs
	"""

	def __init__(self, shape, dtype="float32", **kwargs) -> None:
		super().__init__(shape, dtype, **kwargs)

		self.fan_in, self.fan_out = kwargs.get("inout") or shape
		fan_avg = (self.fan_in + self.fan_out) / 2
		self.r = np.sqrt(3 / fan_avg)

	def call(self, *args, **kwargs):
		return np.random.uniform(-self.r, self.r, size=self.shape)