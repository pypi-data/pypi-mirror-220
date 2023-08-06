from bren.nn.optimisers import Optimiser
from bren import Constant


class SGD(Optimiser):
	def __init__(self, learning_rate=0.01, beta=0) -> None:
		super().__init__()
		self.learning_rate = learning_rate
		self.beta = beta 
		self.momentum = []

	def initialise(self, len):
		for _ in range(len): self.momentum.append(Constant(0))

	def apply_gradients(self, vars, grads, **kwargs): 
		if len(self.momentum) == 0: self.initialise(len(vars))
		self.update(vars, grads, self.momentum)

	def update(self, var, grad, momentum): 
		m = momentum.assign((self.beta * momentum) - (self.learning_rate * grad)) 
		var.assign_add(m)

