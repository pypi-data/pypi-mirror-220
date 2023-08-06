import numpy as np
from bren.autodiff.nodes import (Operator, Graph)
import inspect


np.seterr(invalid="ignore", divide="ignore")

OPS = {}

def custom(grad, funcname=None):
	class operator(Operator):
		count = 0

		def __init__(self, inputs, value=None, name=funcname, **kwargs) -> None:
			super().__init__(inputs, value, name, **kwargs)
			if Graph._g: Graph._g.add(self)
			self.name = self.set_name(operator, name=name)
			self.grad = grad
			operator.count += 1

	return operator


def custom_gradient(grad):
	"""
	A decorator which maps a custom gradient to a function.
	[NOTE] This is advised for functions which perform logical operations.
	
	Parameters 
	----------
	grad: The gradient of the function which is being decorated.

	"""
	def decorator(func):
		OPS[func.__name__ + " (vectorized)"] = custom(grad)
		return np.frompyfunc(func, nin=inspect.signature(func).parameters.__len__(), nout=1)

	return decorator 


def ufunc_grad(*_ufunc_name):
	def decorator(grad):
		for name in _ufunc_name:
			OPS[name] = custom(grad, funcname=name)
		return grad

	return decorator


@ufunc_grad("nongrad")
def default_grad(*ab, dout, **kwargs): return dout, dout

@ufunc_grad(np.abs.__name__, np.absolute.__name__)
def absolute_grad(a, dout, **kwargs): return [np.multiply(dout, (a / np.abs(a)))]

@ufunc_grad(np.add.__name__)
def add_grad(a, b, dout, **kwargs): return dout, dout

@ufunc_grad(np.arccos.__name__)
def arccos_grad(a, dout, **kwargs): return [np.multiply(dout, -(1 / (np.sqrt(1 - (a ** 2)))))]
@ufunc_grad(np.arccosh.__name__)
def arccosh_grad(a, dout, **kwargs): return [np.multiply(dout, (1 / (np.sqrt((a ** 2) - 1))))]

@ufunc_grad(np.arcsin.__name__)
def arcsin_grad(a, dout, **kwargs): return [np.multiply(dout, (1 / (np.sqrt(1 - (a ** 2)))))]
@ufunc_grad(np.arcsinh.__name__)
def arcsinh_grad(a, dout, **kwargs): return [np.multiply(dout, (1 / (np.sqrt((a ** 2) + 1))))]

@ufunc_grad(np.arctan.__name__)
def arctan_grad(a, dout, **kwargs): return [np.multiply(dout, (1 / ((a ** 2) + 1)))]
@ufunc_grad(np.arctanh.__name__)
def arctanh_grad(a, dout, **kwargs): return [np.multiply(dout, (1 / (1 - (a ** 2))))]

@ufunc_grad(np.cbrt.__name__)
def cbrt_grad(a, dout, **kwargs): return [np.multiply(dout, (1 / ((3 * a) ** (2 / 3))))]

@ufunc_grad(np.cos.__name__)
def cos_grad(a, dout, **kwargs): return [np.multiply(dout, -np.sin(a))]
@ufunc_grad(np.cosh.__name__)
def cosh_grad(a, dout, **kwargs): return [np.multiply(dout, np.sinh(a))]

@ufunc_grad(np.divide.__name__)
def divide_grad(a, b, dout, **kwargs):
	return (np.divide(dout, b), -np.multiply(dout, (a / (b ** 2))))

@ufunc_grad(np.exp2.__name__)
def exp2_grad(a, dout, **kwargs): return [np.multiply(dout, (np.log(2) * (2 ** a)))]

@ufunc_grad(np.exp.__name__)
def exp_grad(a, dout, **kwargs): return [np.multiply(dout, np.exp(a))]

@ufunc_grad(np.log10.__name__)
def log10_grad(a, dout, **kwargs): return [np.multiply(dout, (1 / (np.log(10) * a)))]

@ufunc_grad(np.log1p.__name__)
def log1p_grad(a, dout, **kwargs): return [np.multiply(dout, (1 / (a + 1)))]

@ufunc_grad(np.log2.__name__)
def log2_grad(a, dout, **kwargs): return [np.multiply(dout, (1 / np.log(2) * a))]

@ufunc_grad(np.log.__name__)
def log_grad(a, dout, **kwargs): return [np.multiply(dout, (1 / a))]

@ufunc_grad(np.matmul.__name__)
def matmul_grad(a, b, dout, **kwargs):
	return np.matmul(dout, b.T), np.matmul(a.T, dout)

@ufunc_grad(np.multiply.__name__)
def multiply_grad(a, b, dout, **kwargs): return np.multiply(dout, b), np.multiply(dout, a)

@ufunc_grad(np.negative.__name__)
def negative_grad(a, dout, **kwargs): return [np.negative(dout)]

@ufunc_grad(np.power.__name__)
def power_grad(a, b, dout, **kwargs):
	return (np.multiply(dout, (b * (a ** (b - 1)))),
	np.nan_to_num(np.multiply(dout, (a ** b) * (np.log(a))), nan=0, neginf=0, posinf=0))

@ufunc_grad(np.reciprocal.__name__)
def reciprocal_grad(a, dout, **kwargs): return [np.multiply(dout, -np.reciprocal(a ** 2))]

@ufunc_grad(np.sin.__name__)
def sin_grad(a, dout, **kwargs): return [np.multiply(dout, np.cos(a))]
@ufunc_grad(np.sinh.__name__)
def sinh_grad(a, dout, **kwargs): return [np.multiply(dout, np.cosh(a))]

@ufunc_grad(np.sqrt.__name__)
def sqrt(a, dout, **kwargs): return [np.multiply(dout, 1 / (2 * np.sqrt(a)))]

@ufunc_grad(np.subtract.__name__)
def subtract_grad(a, b, dout, **kwargs): return dout, np.negative(dout)

@ufunc_grad(np.tan.__name__)
def tan_grad(a, dout, **kwargs): 
	return [np.multiply(dout, 1 + (np.tan(a) ** 2))]

@ufunc_grad(np.tanh.__name__)
def tanh_grad(a, dout, **kwargs): return [np.multiply(dout, 1 - (np.tanh(a) ** 2))]

@ufunc_grad(np.transpose.__name__)
def transpose_grad(a, dout, **kwargs): return [dout.T]

@ufunc_grad(np.mean.__name__)
def mean_grad(a, dout, **kwargs): return [np.divide(dout, a.size)]
