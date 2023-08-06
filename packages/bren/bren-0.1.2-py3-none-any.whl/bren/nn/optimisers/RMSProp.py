from bren.nn.optimisers import Optimiser
from bren import Constant
import numpy as np


class RMSProp(Optimiser):
	def __init__(self, learning_rate=0.001, beta=0.9, epsilon=10e-10) -> None:
		super().__init__()
		self.learning_rate = learning_rate
		self.beta = beta
		self.epsilon = epsilon
		self.s = []

	def initialise(self, len):
		for _ in range(len): self.s.append(Constant(0))

	def apply_gradients(self, vars, grads, **kwargs):
		if len(self.s) == 0: self.initialise(len(vars))
		self.update(vars, grads, self.s)

	def update(self, var, grad, s):
		_s = s.assign((self.beta * s) + (1 - self.beta) * (grad ** 2))
		_t = (self.learning_rate * grad) / (np.sqrt(_s + self.epsilon))
		var.assign_sub(_t / (1 - self.beta))