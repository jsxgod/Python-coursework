import numpy as np

sigmoid = (
    lambda x: 1./(1 + np.exp(-x)),
    lambda x: x * (1. - x)
)

relu = (
    lambda x: np.maximum(0, x),
    lambda x: 1. * (x > 0)
)

tanh = (
    lambda x: np.tanh(x),
    lambda x: 1-x**2
)


def mse(x1, x2):
    result = 0
    for index, result in enumerate(x1):
        result += (result - x2[index]) ** 2
    return result/len(x1)
