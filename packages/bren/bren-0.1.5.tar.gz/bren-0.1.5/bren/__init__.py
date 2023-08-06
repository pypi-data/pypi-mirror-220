"""
bren
====
bren is a custom [numpy](https://numpy.org) based library, powered by automatic differentiation,
inspired by [Tensorflow](https://www.tensorflow.org)/[Keras](https://keras.io), which allows users to build small scale simple neural networks. It's analogous yet simpler design to the Keras api allows users to produce, train and save their own models, with custom components, without having to learn an entirely new structure. 

bren is part of a sequence of neural network from scratch projects and a successor to the [neural-network-from-scratch-v2](https://github.com/OmPanchal/nn-from-scratch-2), with one major update being the integration of automatic differentitation. Automatic differentiation allows for the real-time determination of derivatives during back propagation and reduces the need for users to couple mathematical computation with derivatives as was required in the previous projects.

Examples tend to import `bren` as `br`
```python
import bren as br

A = br.Variable([1, 2, 3])
print(A + 2) # <Variable value=[3. 4. 5.] dtype=float64>
```

Autodiff
--------
Bren is an autodiff driven neural network library, with backpropagation making use of `br.Graph` to find the derivatives of the trainable parameters with respect to the loss. This is governed by `br.Variable` which keeps track of any operation which have been performed on the `Variable` object.

```python
import bren as br

A = br.Variable([1, 2, 3], dtype="float64")

with br.Graph() as g:
	B = A ** 2 # any computation performed on a Variable will be tracked in a with statement
	print(g.grad(B, [A])) # [<Constant value=[2. 4. 6.] dtype=float64>]
```
"""


from bren.core.core import Constant, Variable
from bren.autodiff.nodes.Graph import Graph
import bren.nn as nn
from bren.autodiff.operations.ops import custom_gradient



__all__ = [nn, Constant, custom_gradient, Graph, Variable]