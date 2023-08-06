from bren.nn.optimisers import Optimiser
from bren import Constant
import numpy as np


class Adam(Optimiser):
	def __init__(self, learning_rate=0.001, beta1=0.9, beta2=0.999, epsilon=10e-10) -> None:
		super().__init__()
		self.learning_rate = learning_rate
		self.beta1 = beta1
		self.beta2 = beta2
		self.epsilon = epsilon
		self.s = []
		self.m = []

	def initialise(self, len):
		for _ in range(len):
			self.s.append(Constant(0))
			self.m.append(Constant(0))
		 
	def apply_gradients(self, vars, grads, **kwargs):
		if len(self.s) == 0 and len(self.m) == 0:
			self.initialise(len(vars))

		self.update(vars, grads, self.m, self.s)

	def update(self, var, grad, m, s):
		_m = m.assign((self.beta1 * m) - ((1 - self.beta1) * grad))
		_s = s.assign((self.beta2 * s) + (1 - self.beta2) * (grad ** 2))

		m_hat = _m / (1 - self.beta1)
		s_hat = _s / (1 - self.beta2) 

		_t = (self.learning_rate * m_hat) / np.sqrt(s_hat + self.epsilon)

		var.assign_add(_t)
	