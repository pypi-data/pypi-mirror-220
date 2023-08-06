class Initialiser(object):
	"""
	The base Initialiser class
	"""
	def __init__(self, shape, dtype="float32", **kwargs) -> None:
		self.shape = shape
		self.dtype = dtype

	def __call__(self, *args, **kwargs): 
		return self.call(**self.__dict__).astype(self.dtype)

	def call(self, shape, *args, **kwargs):
		"""
		Where the functionaliry of the initialiser takes place

		Parameters
		----------
		shape (`tuple`): the shape of the input
		"""
		...


def initialiser_from_func(func):
	"""
	Used to produce an Initialiser class with a custom function

	Parameters
	----------
	func (`function`): the intitalisation function
	"""
	class Initialiser(object):
		def __init__(self, shape, dtype="float32", **kwargs) -> None:
			self.shape = shape
			self.dtype = dtype

		def __call__(self, *args, **kwargs): 
			return func(**self.__dict__).astype(self.dtype)

	return Initialiser