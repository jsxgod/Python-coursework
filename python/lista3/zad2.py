

def flatten(lst):
    for element in lst:
        if isinstance(element, list):
            yield from flatten(element)
        else:
            yield element


example_lst = [[1, 2, ["a", 4, "b", 5, 5, 5]], [4, 5, 6 ], 7, [[9, [123, [[123]]]], 10]]

print(example_lst)
print(list(flatten(example_lst)))