import numpy as np
import requests, gzip, os, pathlib
from bren import Variable


path = os.path.join(pathlib.Path(__file__).parent.resolve(), "data")


def fetch(url):
	"""
	Fetches files from a given url
	"""
	if os.path.isfile(path):
		with open(path, "rb") as f:
			data = f.read()
	else:
		with open(path, "wb") as f:
			data = requests.get(url).content
			f.write(data)
	os.remove(path)
	return np.frombuffer(gzip.decompress(data), dtype=np.uint8).copy()


def load_mnist(dtype="float64"):
	"""
	Loads the mnist dataset and converts the data into a tuple of `br.Variable`

	Parameters
	----------
	dtype (`str`): Determines the data type of the dataset

	Returns
	-------
	Returns a tuple of length 4 with the training features, training lables, testing features and testing lables respectively.
	"""
	X = fetch("http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz")[0x10:].reshape((-1, 28, 28)) / 255.
	Y = fetch("http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz")[8:] 
	X_test = fetch("http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz")[0x10:].reshape((-1, 28, 28)) / 255.
	Y_test = fetch("http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz")[8:]
	return (Variable(X, dtype=dtype), Variable(Y, dtype=dtype), 
		 Variable(X_test, dtype=dtype), Variable(Y_test, dtype=dtype))
