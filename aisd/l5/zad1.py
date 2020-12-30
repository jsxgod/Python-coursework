import sys
from collections import deque

from utils import has_label, are_labeled


class Node(dict):
    def __cmp__(self, other):
        if self['priority'] < other['priority']:
            return -1
        elif self['priority'] == other['priority']:
            return 0
        else:
            return 1

    def __eq__(self, another):
        return self['priority'] == another['priority']

    def __getattr__(self, attr):
        return self.get(attr, None)


class PriorityQueue:
    def __init__(self, nodes):
        self.size = 0
        self.heap = deque([None])
        self.labeled = False
        for n in nodes:
            self.insert(n)
        if are_labeled(nodes):
            self.labeled = True
            self.position = {node.label: i+1 for i, node in enumerate(self.heap) if i > 0}

    def __eq__(self, other):
        return list(self.heap)[1:] == other

    def node(self, i):
        return dict(index=i, value=self.heap[i])

    def parent(self, child):
        i = child['index']
        p = i // 2
        return self.node(p)

    def children(self, parent):
        p = parent['index']
        l, r = (p * 2), (p * 2 + 1)
        if r > self.size:
            return [self.node(l)]
        else:
            return [self.node(l), self.node(r)]

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        if self.labeled:
            I, J = self.heap[i], self.heap[j]
            self.position[I.label] = i
            self.position[J.label] = j

    def shift_up(self, i):
        p = i // 2
        while p:
            if self.heap[i].priority < self.heap[p].priority:
                self.swap(i, p)
            i = p
            p = p // 2

    def priority(self, q, p):
        while True:
            try:
                i = self.position[q]
                self.pop(i)
                self.insert(q, p)
            except:
                break

    def shift_down(self, i):
        c = i * 2
        while c <= self.size:
            c = self.min_child(i)
            if self.heap[i].priority > self.heap[c].priority:
                self.swap(i, c)
            i = c
            c = c * 2

    def min_child(self, i):
        l, r = (i * 2), (i * 2 + 1)
        if r > self.size:
            return l
        else:
            return l if self.heap[l].priority < self.heap[r].priority else r

    def empty(self):
        if self.size == 0:
            return True
        else:
            return False

    def min(self):
        return self.heap[1]

    def top(self):
        return self.min

    def shift(self):
        return self.pop(1)

    def pop(self, i):
        if self.size == 0:
            return None
        v = self.heap[i]
        self.swap(self.size, i)
        self.heap.pop()
        self.size -= 1
        self.shift_down(i)
        return v

    def insert(self, value, priority):
        self.insert2(Node(label=value, priority=priority))

    def insert2(self, node):
        if has_label(node) and self.labeled:
            self.position[node.label] = self.size
        self.heap.append(node)
        self.size += 1
        self.shift_up(self.size)

    def print(self):
        string = ""
        sorted = [self.shift() for i in range(self.size)]
        for i in range(len(sorted)):
            string += ('(' + str(sorted[i].label) + ',' + str(sorted[i].priority) + ')')
            if i + 1 < len(sorted):
                string += ' '
        self.heap = deque([None] + sorted)
        self.size = len(self.heap) - 1
        return string


M = int(input())
queue = PriorityQueue([])
for _ in range(M):
    operation = input().split(' ')
    if operation[0] == 'insert':
        if len(operation) == 3:
            queue.insert(operation[1], operation[2])
    elif operation[0] == 'empty':
        if queue.size == 0:
            print('1')
        else:
            print('0')
    elif operation[0] == 'top':
        if queue.size == 0:
            print("")
        else:
            x = queue.min()
            print('(' + str(x.label) + ',' + str(x.priority) + ')')
    elif operation[0] == 'pop':
        if queue.size == 0:
            print("")
        else:
            x = queue.pop(1)
            print('(' + str(x.label) + ',' + str(x.priority) + ')')
    elif operation[0] == 'priority':
        if len(operation) == 3:
            queue.priority(operation[1], operation[2])
    elif operation[0] == 'print':
        print(queue.print())
    else:
        sys.stderr.write('Invalid input\n')
