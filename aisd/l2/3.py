import sys
import pandas as pd
import numpy as np
from timeit import default_timer as timer
import random
from itertools import chain

assert len(sys.argv) == 8

sort = sys.argv[2]
comparator = sys.argv[4]
file_name = sys.argv[6]
k_iterations = int(sys.argv[7])

global comparisons
global swaps
assert comparator in ["<=", ">="]
assert sort in ["quick", "dpquick"]


def compare(x, y) -> bool:
    global comparisons
    comparisons += 1

    if comparator == "<=":
        return x <= y
    else:
        return x >= y


def compare_sharp(x, y) -> bool:
    global comparisons
    comparisons += 1

    if comparator == "<=":
        return x < y
    else:
        return x > y


def quick_sort(array, start, end):
    if start >= end:
        return

    p = partition(array, start, end)
    quick_sort(array, start, p-1)
    quick_sort(array, p+1, end)

    return array


def partition(array, start, end) -> int:
    global swaps

    pivot = array[start]
    low = start + 1
    high = end

    while True:
        while low <= high and compare(pivot, array[high]):
            high -= 1
        while low <= high and compare(array[low], pivot):
            low += 1

        if low <= high:
            swaps += 1
            array[low], array[high] = array[high], array[low]
        else:
            break

    swaps += 1
    array[start], array[high] = array[high], array[start]

    return high

def dpquicksort(list):
    global swaps
    n = len(list)
    if n <= 1:
        return list
    elif n == 2:
        if comparator == "<=":
            return sorted(list)
        else:
            return sorted(list, reverse=True)

    pivot1, pivot2 = list.pop(0), list.pop(0)
    if not compare(pivot1, pivot2):
        pivot1, pivot2 = pivot2, pivot1

    a = []
    b = []
    c = []
    for element in list:
        if compare_sharp(element, pivot1):
            swaps += 1
            a.append(element)
        elif compare(pivot1, element) and compare_sharp(element, pivot2):
            swaps += 1
            b.append(element)
        else:
            swaps += 1
            c.append(element)
    return dpquicksort(a) + [pivot1] + dpquicksort(b) + [pivot2] + dpquicksort(c)


def generate_data(n) -> []:
    array = []
    for i in range(n):
        array.append(random.SystemRandom().randint(-10000, 10000))
    return array


data = []
data_sorted = []
statistics = []

for size in range(100, 10100, 100):
    print(size)
    for k in range(k_iterations):
        data = generate_data(size)
        comparisons = 0
        swaps = 0
        if sort == "quick":
            start = timer()
            data_sorted = quick_sort(data, 0, size - 1)
            end = timer()
            statistics.append([size, comparisons, swaps, end - start])
            assert all(compare(data_sorted[i], data_sorted[i + 1]) for i in range(len(data_sorted) - 1))
        if sort == "dpquick":
            start = timer()
            data_sorted = dpquicksort(data)
            end = timer()
            statistics.append([size, comparisons, swaps, end - start])
            assert all(compare(data_sorted[i], data_sorted[i + 1]) for i in range(len(data_sorted) - 1))


df = pd.DataFrame(statistics, columns=['Size', 'C', 'S', 'Time'])

df.to_csv(file_name, header=True, index=None, sep=' ', mode='w')
