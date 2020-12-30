import os
import sys
import pandas as pd
import numpy as np
from timeit import default_timer as timer
import random

assert len(sys.argv) == 8

sort = sys.argv[2]
comparator = sys.argv[4]
file_name = sys.argv[6]
k_iterations = int(sys.argv[7])

global comparisons
global swaps
assert comparator in ["<=", ">="]
assert sort in ["insert", "merge", "quick", "quick2", "radix"]


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


def insertion_sort(n, array):
    global swaps
    for i in range(1, len(array)):
        if compare(array[i-1], array[i]):
            continue
        for j in range(i):
            if compare_sharp(array[i], array[j]):
                array[j], array[j + 1:i + 1] = array[i], array[j:i]
                swaps += 1
                break
    return array


def merge_sort(array, left_index, right_index):
    if left_index >= right_index:
        return

    middle_index = (left_index + right_index) // 2
    merge_sort(array, left_index, middle_index)
    merge_sort(array, middle_index + 1, right_index)

    merge(array, left_index, right_index, middle_index)

    return array


def merge(array, left_index, right_index, middle_index):
    global swaps

    left_array = array[left_index : middle_index + 1]
    right_array = array[middle_index + 1 : right_index+1]

    l = 0
    r = 0
    s = left_index

    # Add elements according to comparator function from either left or right sub array
    # until one of them is emptied
    while l < len(left_array) and r < len(right_array):
        if compare(left_array[l], right_array[r]):
            array[s] = left_array[l]
            l += 1
        else:
            swaps += 1
            array[s] = right_array[r]
            r += 1

        s += 1

    # Add remaining elements from either left or right sub array
    for item in left_array[l:]:
        array[s] = item
        s += 1
    for item in right_array[r:]:
        array[s] = item
        s += 1


def quick_sort2(array):
    if len(array) < 2:
        return array

    pivot = array.pop(0)

    return quick_sort2([x for x in array if compare(x, pivot)]) + [pivot] + quick_sort2([x for x in array if compare_sharp(pivot, x)])


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


def countingSort(array, power):
    n = len(array)
    output = [0] * n
    count = [0] * 10

    for element in array:
        digit = (element // (10 ** power)) % 10
        if comparator == "<=":
            count[digit] += 1
        else:
            count[9-digit] += 1

    for i in range(1, 10):
        count[i] += count[i-1]

    for element in reversed(array):
        digit = (element // (10 ** power)) % 10
        if comparator == "<=":
            output[count[digit] - 1] = element
            count[digit] -= 1
        else:
            output[count[9-digit] - 1] = element
            count[9-digit] -= 1

    for i in range(0, n):
        array[i] = output[i]


def radixSort(array):
    max_element = max(array)
    power = 0
    while max_element // 10 ** power > 0:
        countingSort(array, power)
        power += 1
    return array


def generate_data(n) -> []:
    array = []
    for i in range(n):
        # array.append(random.SystemRandom().randint(-10000, 10000))
        array.append(random.SystemRandom().randint(1000000000000000, 100000000000000000000))
    return array


data = []
data_sorted = []
statistics = []

for size in range(100, 10100, 100):
    sys.stderr.write(str(size) + '\n')
    for k in range(k_iterations):
        data = generate_data(size)
        comparisons = 0
        swaps = 0
        if sort == "insert":
            start = timer()
            data_sorted = insertion_sort(size, data)
            end = timer()
            statistics.append([size, comparisons, swaps, end - start])
            assert all(compare(data_sorted[i], data_sorted[i + 1]) for i in range(len(data_sorted) - 1))
        if sort == "merge":
            start = timer()
            data_sorted = merge_sort(data, 0, size - 1)
            end = timer()
            statistics.append([size, comparisons, swaps, end - start])
            assert all(compare(data_sorted[i], data_sorted[i + 1]) for i in range(len(data_sorted) - 1))
        if sort == "quick":
            start = timer()
            data_sorted = quick_sort(data, 0, size - 1)
            end = timer()
            statistics.append([size, comparisons, swaps, end - start])
            assert all(compare(data_sorted[i], data_sorted[i + 1]) for i in range(len(data_sorted) - 1))
        if sort == "quick2":
            start = timer()
            data_sorted = quick_sort2(data)
            end = timer()
            statistics.append([size, comparisons, swaps, end - start])
            assert all(compare(data_sorted[i], data_sorted[i + 1]) for i in range(len(data_sorted) - 1))
        if sort == "radix":
            start = timer()
            data_sorted = radixSort(data)
            end = timer()
            statistics.append([size, comparisons, swaps, end - start])
            assert all(compare(data_sorted[i], data_sorted[i + 1]) for i in range(len(data_sorted) - 1))


df = pd.DataFrame(statistics, columns=['Size', 'C', 'S', 'Time'])

df.to_csv(file_name, header=True, index=None, sep=' ', mode='w')
