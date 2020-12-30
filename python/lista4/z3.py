import random

import numpy as np


def pprint_tree(node, file=None, _prefix="", _last=True):
    if node.data == '1':
        print(_prefix, "ROOT " if _last else "|- ", node.data, sep="", file=file)
    else:
        print(_prefix, "`- " if _last else "|- ", node.data, sep="", file=file)
    _prefix += "     " if _last else "|  "

    child_count = len(node.children)

    for i, child in enumerate(node.children):
        _last = i == (child_count - 1)
        pprint_tree(child, file, _prefix, _last)


class Node:
    def __init__(self, data):
        self.data = data
        self.children = []

    def __str__(self):
        return str(self.data) + ':  [' + ', '.join(map(str, self.children)) + ']'


class Tree:
    def __init__(self, height, root: Node):
        self.root = root
        self.height = height

    def __str__(self):
        return '[' + str(self.root)

    @staticmethod
    def random(height, child_probability=0.6):
        node_value = 1
        depth_left = height

        def random_subtree(sub_depth_left):
            nonlocal node_value
            nonlocal child_probability

            node_value += 1
            subtree = Node(str(node_value))

            if sub_depth_left > 0:
                while np.random.uniform() < child_probability and len(subtree.children) < 11:
                    subtree.children.append(random_subtree(sub_depth_left - 1))

            return subtree

        tree = Tree(height, Node(str(node_value)))
        current_node = tree.root

        while depth_left > 0:
            node_value += 1
            depth_left -= 1

            current_node.children.append(Node(node_value))

            while np.random.uniform() < child_probability:  # possible subtrees before base height
                current_node.children.append(random_subtree(depth_left))

            current_node = random.choice(current_node.children)

        assert height == depth(tree.root)
        return tree


def depth(node: Node) -> int:
    if len(node.children) == 0:
        return 0

    return max([0] + [depth(child) for child in node.children]) + 1


def dfs(node: Node):
    if node is not None:
        yield node.data
        for child in node.children:
            yield from dfs(child)


def bfs(node: Node):
    q = [node]
    while len(q) > 0:
        current = q.pop(0)
        for child in current.children:
            q.append(child)
        yield current.data


t = Tree.random(2, 0.6)
print(depth(t.root))

pprint_tree(t.root)
print(str(t))
print(list(dfs(t.root)))
print(list(bfs(t.root)))
