

def subsets(lst: list):
    return [x + [lst[0]] for x in subsets(lst[1:])] + subsets(lst[1:]) if lst else [[]]


lst = [0, 1, 2, 3]
n = len(lst)

powerset = subsets(lst)
pn = len(powerset)

print(powerset)

assert pn == 2 ** n
