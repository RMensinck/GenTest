from copy import error
import numpy as np
import random
from numpy.core.fromnumeric import reshape

from numpy.core.numeric import cross

test1 = np.array([[5, 5, 5], [5, 5, 5], [5, 5, 5], [5, 5, 5], [5, 5,
                                                               5]])  # 5,3
test2 = np.array([[3, 3, 3], [3, 3, 3], [3, 3, 3], [3, 3, 3], [3, 3,
                                                               3]])  # 5,3

test1 = test1.astype(int)
test2 = test2.astype(int)
print(test2)
print(test1)


def crossover(test1, test2):

    if test1.shape != test2.shape: raise error
    if len(test1) != len(test2): raise error
    original_shape = test1.shape
    test2 = test2.flatten()
    test1 = test1.flatten()

    genlength = len(test1)
    crossoverpoint = random.randint(1, genlength - 1)

    new_test1 = np.concatenate(
        (test1[:crossoverpoint], test2[crossoverpoint:]))
    new_test2 = np.concatenate(
        (test2[:crossoverpoint], test1[crossoverpoint:]))

    print(new_test1)
    print(new_test2)

    reshape1 = np.reshape(new_test1, original_shape)
    reshape2 = np.reshape(new_test2, original_shape)

    print(reshape1)
    print(reshape2)

    print(reshape1.shape)


crossover(test1, test2)
