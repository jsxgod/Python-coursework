import sys
from heapq import heappop, heappush
from operator import itemgetter

size = 0


def kruskal(node_list, edge_list):
    global size

    forest = DjSet()
    mst = []
    for n in node_list:
        forest.add(n)

    x = len(node_list) - 1

    for e in sorted(edge_list, key=itemgetter(2)):
        n1, n2, _ = e
        t1 = forest.find(n1)
        t2 = forest.find(n2)
        if t1 != t2:
            mst.append(e)
            x -= 1
            if x == 0:
                return mst

            forest.union(t1, t2)
            if size == 1:
                break


class DjSet(dict):
    global size

    def add(self, item):
        self[item] = item
        size += 1

    def find(self, item):
        parent = self[item]

        while self[parent] != parent:
            parent = self[parent]

        self[item] = parent
        return parent

    def union(self, item1, item2):
        self[item2] = self[item1]
        size -= 1


def prim(s, edge_list):
    V, T = [], {}
    Q = [(0, None, s)]
    while Q:
        _, p, u = heappop(Q)

        if u in V:
            continue
        V.append(u)
        if p is None:
            pass
        elif p in T:
            T[p].append(u)
        else:
            T[p] = [u]
        for e in sorted(edge_list, key=itemgetter(2)):
            x, y, w = e
            if x == u:
                v = y
            elif y == u:
                v = x
            else:
                continue

            heappush(Q, (w, u, v))

    sum = 0
    weight = 0
    print("Wynik w postaci: u, v, waga")
    for v in T:
        for q in T[v]:
            for edge in edge_list:
                if (edge[0] == v and edge[1] == q) or (edge[0] == q and edge[1] == v):
                    weight = edge[2]
                    sum += weight
                    break
            print("%s %s %s" % (v, q, weight))
    print("Waga: {0:.2f}".format(sum))


type = sys.argv[1]
nodes = []
edges = []
n = int(input())
for x in range(n):
    nodes.append(x+1)
m = int(input())
for i in range(m):
    edge = input().split(' ')
    start = int(edge[0])
    end = int(edge[1])
    cost = float(edge[2])
    edges.append([start, end, cost])
if type == 'k':
    tree = kruskal(nodes, edges)
    cost = 0
    print("Wynik w postaci: u, v, waga")
    for val in tree:
        if val[0] < val[1]:
            print(str(val[0]) + ' ' + str(val[1]) + ' ' + str(val[2]))
        else:
            print(str(val[1]) + ' ' + str(val[0]) + ' ' + str(val[2]))
        cost += val[2]

    print("Waga: {0:.2f}".format(cost))
else:
    prim(1, edges)
