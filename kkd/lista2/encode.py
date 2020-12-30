import os
import sys
from collections import defaultdict

import numpy as np
from timer import measure_time
import entropy


class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.code = ''

    def __str__(self):
        print(self.data)

    def isLeaf(self):
        return self.left is None and self.right is None


class Tree:
    def __init__(self):
        self.root = None
        self.nodes = []

    def search(self, value) -> Node:
        return [node for node in self.nodes if node.data[0] == value][0]


def pprint_tree(node: Node, file=None, _prefix="", _last=True):
    print(_prefix, "`- " if _last else "|- ", node.data[0], sep="", file=file)
    _prefix += "   " if _last else "|  "

    children = []
    if node.left is not None:
        children.append(node.left)
    if node.right is not None:
        children.append(node.right)

    child_count = len(children)
    for i, child in enumerate(children):
        _last = i == (child_count - 1)
        pprint_tree(child, file, _prefix, _last)


def generate_codes(node, current_code):
    if node is not None:
        node.code = current_code
        generate_codes(node.left, current_code + '0')
        generate_codes(node.right, current_code + '1')
    else:
        return


def huffman_tree(freq_dict: defaultdict):
    tree = Tree()

    sorted_freq = list({k: v for k, v in sorted(freq_dict.items(), key=lambda item: item[1])}.items())
    parent = Node(0)

    if len(sorted_freq) == 1:
        tree.root = Node('root')
        tree.root.left = Node(sorted_freq[0])
        tree.nodes.append(tree.root)
        tree.nodes.append(tree.root.left)
        generate_codes(tree.root, '')
        return tree

    while sorted_freq:
        if len(sorted_freq) < 2:
            break

        sorted_freq.sort(key=lambda tup: tup[1])

        first, second = sorted_freq[0], sorted_freq[1]

        if first not in [node.data for node in tree.nodes]:
            node1 = Node(first)
            tree.nodes.append(node1)
        else:
            node1 = [node for node in tree.nodes if node.data == first][0]

        if second not in [node.data for node in tree.nodes]:
            node2 = Node(second)
            tree.nodes.append(node2)
        else:
            node2 = [node for node in tree.nodes if node.data == second][0]

        sorted_freq.pop(0)
        sorted_freq[0] = (node1.data[0] + node2.data[0], node1.data[1] + node2.data[1])
        parent = Node(sorted_freq[0])
        parent.left = node1
        parent.right = node2

        tree.nodes.append(parent)

    tree.root = parent
    generate_codes(tree.root, '')
    return tree


def calculate_byte_occurrences(file_bytes):
    byte_dictionary = defaultdict(np.int64)

    for byte in file_bytes:
        if byte in byte_dictionary:
            byte_dictionary[byte] += 1
        else:
            byte_dictionary[byte] = 1

    return byte_dictionary


@measure_time
def my_encode2(path):
    byte_data = []
    with open(path, "r", encoding='utf-8', errors='ignore') as f:
        while True:
            c = f.read(1)
            if not c:
                break
            else:
                byte_data.append(c.encode())
    byte_freq_dict = calculate_byte_occurrences(byte_data)

    t = huffman_tree(byte_freq_dict)

    encoded_message = ''
    code_dict = dict()

    for byte in byte_data:
        if byte in code_dict.keys():
            encoded_message += code_dict[byte]
        else:
            code = t.search(byte).code
            code_dict[byte] = code
            encoded_message += code

    return encoded_message, t, byte_freq_dict, code_dict


@measure_time
def my_encode(path):
    byte_data = []
    with open(path, "r", encoding='utf-8', errors='ignore') as f:
        while True:
            c = f.read(1)
            if not c:
                break
            else:
                byte_data.append(c.encode())
    byte_freq_dict = calculate_byte_occurrences(byte_data)

    t = huffman_tree(byte_freq_dict)

    encoded_message = ''
    code_dict = dict()

    for byte in byte_data:
        if byte in code_dict.keys():
            encoded_message += code_dict[byte]
        else:
            code = t.search(byte).code
            code_dict[byte] = code
            encoded_message += code

    return encoded_message, t, byte_freq_dict, code_dict

@measure_time
def my_decode(message, tree: Tree):
    current_node = tree.root

    decoded = ''
    for c in message:
        if c == '0':
            current_node = current_node.left
        else:  # c == '1'
            current_node = current_node.right
        if current_node.isLeaf():
            decoded += str(current_node.data[0].decode('utf-8'))
            current_node = tree.root
    return decoded


def average_length(freq_dict, code_dict):
    size = sum([pair[1] for pair in freq_dict.items()])
    length = 0
    for byte in freq_dict.keys():
        length += freq_dict[byte] * len(code_dict[byte])

    return length / size


def _to_Bytes(data):
    b = bytearray()
    for i in range(0, len(data), 8):
        b.append(int(data[i:i + 8], 2))
    return bytes(b)


input_file_name = sys.argv[1]
tree_graph_file = open('tree_graph.txt', 'w')
file_decoded = open('decoded.txt', 'w', encoding='utf-8')

encoded_message, tree, freq_dict, code_dict = my_encode(input_file_name)
decoded_message = my_decode(encoded_message, tree)

with open('encoded.bin', 'wb') as f:
    f.write(_to_Bytes(encoded_message))

print(decoded_message, file=file_decoded, end="")

pprint_tree(tree.root, tree_graph_file)
tree_graph_file.close()

entropy.calculate([input_file_name])


def calculate_compression(input_path, encoded_path):
    original = os.path.getsize(input_path)
    compressed = os.path.getsize(encoded_path)
    return original, compressed, round((((original - compressed) / original) * 100), 0)


file_decoded.close()
tree_graph_file.close()

print('Srednia dlugosc kodowania:', average_length(freq_dict, code_dict))
o_s, c_s, percentage = calculate_compression(input_file_name, 'encoded.bin')
print('Kompresja:', percentage, '% rozmiaru pliku przed kompresją.')
print('Przed: ', o_s, 'bajtow.')
print('Po: ', c_s, 'bajtow.')
