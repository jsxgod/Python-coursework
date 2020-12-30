from operator import ge, lt


def qsort(lst):
    if len(lst) <= 1:
        return lst

    pivot = lst.pop()
    partition = lambda op: [n for n in lst if op(n, pivot)]

    return [*qsort(partition(lt)), pivot, *qsort(partition(ge))]


def qsort2(lst):
    if len(lst) <= 1:
        return lst

    pivot = lst.pop()
    return [*qsort2([n for n in lst if n < pivot]), pivot, *qsort2([n for n in lst if n >= pivot])]


lista = [20, 5, 6, 2, 1, 8, 10, 2, 11, 1]

print(qsort(lista))
