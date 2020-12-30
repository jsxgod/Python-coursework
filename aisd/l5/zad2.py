from zad1 import PriorityQueue
from collections import namedtuple
import math

Edge = namedtuple('Edge', ['vertex', 'weight'])


def dijkstra(graph, source):
    parents = []
    distances = []
    start_weight = math.inf
    for edge in graph.get_vertex():
        q = PriorityQueue([])
        for i in graph.get_vertex():
            weight = start_weight
            if source == i:
                weight = 0
            distances.append(weight)
            parents.append(None)

        q.insert(source, 0)

        while not q.empty():
            v_tuple = q.pop(1)
            v = v_tuple.label

            if v_tuple.priority == math.inf:
                return math.inf, math.inf

            for e in graph.get_edge(v):

                candidate_distance = distances[v] + e.weight
                if distances[e.vertex] > candidate_distance:
                    distances[e.vertex] = candidate_distance
                    parents[e.vertex] = v
                    q.insert(e.vertex, distances[e.vertex])

        shortest_path = []
        ending = edge
        while ending is not None:
            shortest_path.append(ending)
            ending = parents[ending]

        shortest_path.reverse()
        print(edge, shortest_path, distances[edge])
        shortest_path.clear()
        distances.clear()
        parents.clear()


class Graph(object):
    def __init__(self, vertex_count):
        self.vertex_count = vertex_count
        self.adjacency_list = [[] for _ in range(vertex_count)]

    def add_edge(self, source, destination, weight):
        assert source <= self.vertex_count
        assert destination <= self.vertex_count
        self.adjacency_list[source].append(Edge(destination, weight))

    def get_edge(self, vertex):
        for e in self.adjacency_list[vertex]:
            yield e

    def get_vertex(self):
        for v in range(self.vertex_count):
            yield v


number_of_vertices = int(input())
number_of_edges = int(input())
g = Graph(number_of_vertices)
for _ in range(0, number_of_edges):
    edges = input().split(' ')
    g.add_edge(int(edges[0]), int(edges[1]), int(edges[2]))

start_point = int(input())
dijkstra(g, start_point)
