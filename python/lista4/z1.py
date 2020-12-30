from functools import wraps
from time import time
import numpy as np


def measure_time(func):
    @wraps(func)
    def time_it(*args, **kwargs):
        start = int(round(time() * 1000))
        try:
            return func(*args, **kwargs)
        finally:
            result = int(round(time() * 1000)) - start
            print(f"Function executed in: {result} ms.")
    return time_it


def quicksort(lst: list) -> list:
    if len(lst) <= 1:
        return lst

    pivot = lst.pop(0)
    return quicksort([x for x in lst if x <= pivot]) + [pivot] + quicksort([x for x in lst if x > pivot])


@measure_time
def first(lst: list):
    if len(lst) <= 1:
        return lst

    pivot = lst.pop(0)
    return quicksort([x for x in lst if x <= pivot]) + [pivot] + quicksort([x for x in lst if x > pivot])


numbers = list(np.random.rand(1000000) * 100)
numbers = first(numbers)
assert all(numbers[i] <= numbers[i+1] for i in range(len(numbers)-1))
