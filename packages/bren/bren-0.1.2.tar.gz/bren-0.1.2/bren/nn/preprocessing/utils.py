import random
import bren as br
import numpy as np

def shuffle(*arrays, seed_range=1000):
    """
    Randomly shuffles the values in the arrays given, using the same seed throughout.

    Parameters
    ----------
    seed_range (`int`): the seed is a positive integer, and is chosen randomly between the range of 0 and `seed_range` 
    """
    seed = random.randint(0, seed_range)

    for array in arrays:
        np.random.seed(seed)
        np.random.shuffle(array)

    
def split_uneven(array, split):
    """
    Splits an array into a specified number of sub-arrays and appends the remainders to the end of the array.

    Parameters
    ----------
    array (`br.Variable`, `list`): The array.
    split (`int`): The number of sub arrays which you want to split the array into.

    Returns
    -------
    Returns a `br.Variable` of the array split into the number of sub arrays as by `split` along with the remainders at the end of the array
     """

    remainder = len(array) % split
    return br.Variable(np.split(array[:len(array) - remainder], split))