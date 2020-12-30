import copy
import sys
import random
import numpy as np

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


n = int(input("Please enter size:  "))
k = int(input("Please enter position k:  "))

assert k <= n

if mode == '-r':
    data = list(np.random.randint(0, 10000, n))
else:
    data = [x for x in range(1, n+1)]
    np.random.shuffle(data)

data_copy = copy.deepcopy(data)

print('Expected result: ', sorted(data)[k-1])

# Randomized select
swaps = 0
comparisons = 0
rs_result = randomized_select(data, 0, n - 1, k)
print('RANDOMIZED SELECT')
print(rs_result)
print('Comparisons: ', comparisons)
print('Swaps: ', swaps)
print('---------------------------------')

# Select
swaps = 0
comparisons = 0
s_result = select(data_copy, k - 1, pick_pivot)
for i in range(0, len(data_copy)):
    if data_copy[i] == s_result:
        data_copy[i] = [data_copy[i]]
        s_result = data_copy
        break

print('SELECT')
print(s_result)
print('Comparisons: ', comparisons)
print('Swaps: ', swaps)
print('---------------------------------')


