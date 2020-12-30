import numpy as np


def pprint_tree(node, file=None, _prefix="", _last=True):
    if node[0] == '1':
        print(_prefix, "ROOT " if _last else "|- ", node[0], sep="", file=file)
    else:
        print(_prefix, "`- " if _last else "|- ", node[0], sep="", file=file)
    _prefix += "     " if _last else "|  "

    children = [child for child in node[1:] if child is not None]
    child_count = len(children)

    for i, child in enumerate(children):
        _last = i == (child_count - 1)
        pprint_tree(child, file, _prefix, _last)


def random_tree(height: int) -> list:
    """
    Tree has the structure of a list of lists.
    The first item in every list is the node's value.

    tree = [value, left_node, right_node]
    node structure:
        node[0] - value
        node[1] - left node or None
        node[2] - right node or None
    """
    node_value = 1
    depth_left = height

    # tree is the root list holding all sub lists in it
    tree = [str(node_value), None, None]
    current_node = tree

    while depth_left > 0:
        node_value += 1
        depth_left -= 1
        if np.random.uniform() > 0.5:  # current node set to left child
            current_node[1] = [str(node_value), None, None]
            current_node[2], node_value = random_subtree(depth_left, node_value)
            current_node = current_node[1]
        else:  # current node set to right child
            current_node[2] = [str(node_value), None, None]
            current_node[1], node_value = random_subtree(depth_left, node_value)
            current_node = current_node[2]

    assert depth(tree) == height
    return tree


def random_subtree(depth_left, current_value):  # recursively generates random subtree
    if depth_left < 1:
        return None, current_value

    current_value += 1
    tree = [str(current_value), None, None]
    if np.random.uniform() > 0.5:
        tree[1], current_value = random_subtree(depth_left - 1, current_value)
    if np.random.uniform() > 0.5:
        tree[2], current_value = random_subtree(depth_left - 1, current_value)

    return tree, current_value


def depth(node: list) -> int:
    if node[1] is None and node[2] is None:
        return 0
    elif node[1] is None:
        return depth(node[2]) + 1
    elif node[2] is None:
        return depth(node[1]) + 1
    else:
        return max(depth(node[1]), depth(node[2])) + 1


def dfs(tree):
    if tree is not None:
        yield tree[0]
        yield from dfs(tree[1])
        yield from dfs(tree[2])


def bfs(tree):
    q = [tree]
    while len(q) > 0:
        current = q.pop(0)
        if current[1] is not None:
            q.append(current[1])
        if current[2] is not None:
            q.append(current[2])
        yield current[0]


t = random_tree(5)
pprint_tree(t)
print('Depth: ', depth(t))
print(t)
print('DFS: ', *dfs(t))
print('BFS: ', *bfs(t))
