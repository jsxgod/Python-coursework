import random
import sys
import math
import numpy as np
from timeit import default_timer as timer

global comparisons

if len(sys.argv) == 2:
    k = int(sys.argv[1])
else:
    k = 1


def compare_sharp(x, y):
    global comparisons
    comparisons += 1

    return x < y


def equal(x, y):
    global comparisons
    comparisons += 1

    return x == y


def binary_search(data, value):
    if data:
        mid = len(data) // 2
        if equal(data[mid], value):
            return 1
        elif compare_sharp(value, data[mid]):
            return binary_search(data[:mid], value)
        else:
            return binary_search(data[mid+1:], value)
    else:
        return 0


size = 1000
low = 0
high = size*10

comparisons_list = []
times = []
statistics = []

while size <= 100000:
    comparisons_list = []
    times = []
    data = list(np.random.randint(low, high, size))

    sys.stderr.write(str(size) + '\n')
    for _ in range(k):
        number = random.choice(sorted(data))
        comparisons = 0
        start = timer()
        result = binary_search(sorted(data), number)
        end = timer()

        comparisons_list.append(comparisons)
        times.append(end - start)

    statistics.append([size, (max(times), min(times)), (max(comparisons_list), min(comparisons_list))])


    size += 1000

print(statistics, file=open('binary_statistics.txt', 'w'))
