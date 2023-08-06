class Node(object):
	def __init__(self, value, name) -> None:
		self.value = value
		self._gradient = 0
		self.name = name

	def set_name(self, cls, name=None): return f"{name or cls.__name__}/{cls.count}"

	@property
	def gradient(self): return self._gradient
	@gradient.setter
	def gradient(self, value):
		self._gradient = value