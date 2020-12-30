from functools import wraps
from time import time


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

