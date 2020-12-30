import copy
import sys
import random
import numpy as np
import pandas as pd
from timeit import default_timer as timer

mode = sys.argv[1]
assert mode in ["-r", "-p"]
global swaps
global comparisons


def compare(x, y):
    global comparisons
    comparisons += 1
    return x <= y


def compare_sharp(x, y):
    global comparisons
    comparisons += 1
    return x < y


def equal(x, y):
    global comparisons
    comparisons += 1
    return x == y


def partition(data, left, right):
    global swaps
    pivot_index = random.randint(left, right)

    data[right], data[pivot_index] = data[pivot_index], data[right]

    i = left
    for j in range(left + 1, right + 1):
        if compare(data[j], data[left]):
            i += 1
            data[i], data[j] = data[j], data[i]
            swaps += 1

    data[i], data[left] = data[left], data[i]
    swaps += 1

    return i


def randomized_select(items, left, right, k):
    if items is None or len(items) < 1:
        return None
    if left == right:
        data[left] = [data[left]]
        return data

    i = partition(data, left, right)

    if k - 1 == i:
        data[i] = [data[i]]
        return data
    elif k <= i:
        return randomized_select(data, left, i - 1, k)
    else:
        return randomized_select(data, i + 1, right, k)


def nlogn_median(data):
    data = sorted(data)
    if len(data) % 2 == 1:
        return data[len(data) // 2]
    else:
        return 0.5 * (data[len(data) // 2 - 1] + data[len(data) // 2])


def select_median(data, pivot_fn=random.choice):
    if len(data) % 2 == 1:
        return select(data, len(data) / 2, pivot_fn)
    else:
        return 0.5 * (select(data, len(data) / 2 - 1, pivot_fn) +
                      select(data, len(data) / 2, pivot_fn))


def select(data, k, pivot_fn):
    if len(data) == 1:
        return data[0]

    pivot = pivot_fn(data)

    left = [x for x in data if compare_sharp(x, pivot)]
    right = [x for x in data if compare_sharp(pivot, x)]
    pivots = [x for x in data if equal(x, pivot)]

    if k < len(left):
        return select(left, k, pivot_fn)
    elif k < len(left) + len(pivots):
        return pivots[0]
    else:
        return select(right, k - len(left) - len(pivots), pivot_fn)


def pick_pivot(data):
    assert len(data) > 0

    if len(data) < 5:

        return nlogn_median(data)

    subs = [data[i:i + 5] for i in range(0, len(data), 5)]

    full_subs = [sub for sub in subs if len(sub) == 5]

    sorted_groups = [sorted(sub) for sub in full_subs]

    medians = [sub[2] for sub in sorted_groups]

    median_of_medians = select_median(medians, pick_pivot)
    return median_of_medians


low = 10
high = 100000

step = 2

s_statistics = []
rs_statistics = []

size = low
while size <= high:
    k = random.choice([*range(1, size+1)])
    if mode == '-r':
        data = list(np.random.randint(0, size*100, size))
    else:
        data = [x for x in range(1, size+1)]
        np.random.shuffle(data)

    data_copy = copy.deepcopy(data)

    # Randomized select
    swaps = 0
    comparisons = 0
    start = timer()
    randomized_select(data, 0, size - 1, k)
    end = timer()
    rs_statistics.append([size, comparisons, swaps, end - start])
    # Select
    swaps = 0
    comparisons = 0
    start = timer()
    select(data_copy, k - 1, pick_pivot)
    end = timer()
    s_statistics.append([size, comparisons, swaps, end - start])

    if step == 2:
        size *= 5
        step = 5
    elif step == 5:
        size *= 2
        step = 2


rs_df = pd.DataFrame(rs_statistics, columns=['Size', 'C', 'S', 'Time'])
s_df = pd.DataFrame(s_statistics, columns=['Size', 'C', 'S', 'Time'])

rs_df.to_csv('r_select.txt', header=True, index=None, sep=' ', mode='w')
s_df.to_csv('select.txt', header=True, index=None, sep=' ', mode='w')
