import bren.autodiff.nodes as nodes


class Const(nodes.Node):
	count = 0

	def __init__(self, value, name=None) -> None:
		self.name = name or self.set_name(Const) 
		Const.count += 1
		if nodes.Graph._g: nodes.Graph._g.add(self)
		super().__init__(value, self.name)
	
	def __repr__(self) -> str:
		return f"<{Const.__name__} name={self.name} value={self.value}>"

	@nodes.Node.gradient.setter
	def gradient(self, value): ...