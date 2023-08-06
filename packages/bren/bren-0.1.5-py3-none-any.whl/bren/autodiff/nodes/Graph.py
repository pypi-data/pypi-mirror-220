import numpy as np
import bren.autodiff.nodes as nodes
import bren as br


class Graph(object):

	"""
	The Graph object helps keep track of all of the operations performed on a Variable object. In doing so, it performs a backward pass and computes the gradients of all of the Variables involved in the computation graph. 
	"""

	_g = None

	def __init__(self) -> None:
		self.nodes = set()
		Graph._g = self.nodes

	def __reset_counts(self, root):
		if hasattr(root, "count"):
			root.count = 0
		else: 	
			for child in root.__subclasses__():
				self.__reset_counts(child)

	def __reset_session(self):
		try:
			del Graph._g
		except: pass

		Graph._g = None
		self.__reset_counts(nodes.Node)
		self.__reset_counts(nodes.Operator)

	def __enter__(self):
		Graph._g.add("entered graph")
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.__reset_session()

	def __g(self, dy, dx):
		op = [dy._source]
		dy._source.gradient = np.ones(shape=dy.shape, dtype=dy.dtype)

		for x in dx:
			x._source.gradient = 0 

		for operation in op:
			try:
				grads = operation(dout=operation.gradient)

				for inp, grad in zip(operation.inputs, grads):
					if inp: inp.gradient += grad

					if isinstance(inp, nodes.Operator):
						op.append(inp)

			except AttributeError:
				raise Exception("Cannot find gradient of 2 unconnected variables")

		for value in dx:
			yield br.Constant(value._source.gradient, dtype=value.dtype)

	def grad(self, dy, dx): 
		"""
		Performs a backward pass and returns a list of 
		"""
		return list(self.__g(dy, dx))
