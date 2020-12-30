import sys

sort = sys.argv[2]
comparator = sys.argv[4]

comparisons = 0
swaps = 0

assert comparator in ["<=", ">="]
assert sort in ["insert", "merge", "quick"]


def compare(x, y) -> bool:
    global comparisons
    comparisons += 1

    if comparator == "<=":
        return x <= y
    else:
        return x >= y


def insertion_sort(n, array):
    global swaps
    for i in range(1, len(array)):
        if compare(array[i-1], array[i]):
            continue
        for j in range(i):
            if compare(array[i], array[j]):
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


data = []
n = int(input("Please enter size:\n"))
size = n
numbers = input("Please enter numbers: ")
for number in numbers.split(' '):
    if size > 0:
        data.append(int(number))
        size -= 1
    else:
        break

print(data)

data_sorted = []

if sort == "insert":
    data_sorted = insertion_sort(n, data)
if sort == "merge":
    data_sorted = merge_sort(data, 0, n-1)
if sort == "quick":
    data_sorted = quick_sort(data, 0, n-1)

print("Size: ", n)
print("Sorted: ", data_sorted)
print("Comparisons: ", comparisons)
print("Swaps: ", swaps)


assert all(compare(data_sorted[i], data_sorted[i+1]) for i in range(len(data_sorted)-1))
