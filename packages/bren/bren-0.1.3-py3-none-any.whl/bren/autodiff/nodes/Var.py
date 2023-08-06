import bren.autodiff.nodes as nodes


class Var(nodes.Node):
	count = 0

	def __init__(self, value, name=None) -> None:
		self.name = name or self.set_name(Var) 
		Var.count += 1
		if nodes.Graph._g: nodes.Graph._g.add(self)
		super().__init__(value, self.name)
	
	def __repr__(self) -> str:
		return f"<{Var.__name__} name={self.name} value={self.value}>"