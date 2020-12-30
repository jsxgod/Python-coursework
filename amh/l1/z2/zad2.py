import random
import sys
import time
from copy import deepcopy


def neighbors_from_data(data):
    neighbors = {}

    for i, line in enumerate(data):
        if i == 0:
            continue
        lst = list()
        for j, cost in enumerate(line, 1):
            if j == i:
                continue
            lst.append((j, int(cost)))
        neighbors[i] = lst

    return neighbors


def default_path(neighbors: dict):
    start_city = list(neighbors.keys())[0]
    selected_neighbor = int()

    path = []

    current_city = start_city

    total_cost = 0
    while current_city not in path:
        lowest_cost = 1000000000
        for neighbor in neighbors[current_city]:
            if neighbor[1] < lowest_cost and neighbor[0] not in path:
                selected_neighbor = neighbor[0]
                lowest_cost = neighbor[1]

        path.append(current_city)
        if lowest_cost != 1000000000:
            total_cost += lowest_cost
        current_city = selected_neighbor

    path.append(start_city)
    total_cost += neighbors[current_city][0][1]

    return path, total_cost


def shake_path(path: list):
    city = random.randrange(1, len(path)-1)
    city2 = random.choice([c for c in range(1, len(path) - 1) if c != city])
    cities = sorted([city, city2])
    city, city2 = cities[0], cities[1]
    if random.random() < 0.7:
        path[city], path[city2] = path[city2], path[city]
        return path
    return path[:city] + list(reversed(path[city:city2])) + path[city2:]


def calculate_cost(path: list, neighbors: dict):
    cost = 0
    for city, next_city in zip(path, path[1:]):
        if next_city < city:
            cost += neighbors[city][next_city-1][1]
        else:
            cost += neighbors[city][next_city-2][1]

    return cost


def tabu_search(start_path, tabu_length, num_of_shakes, time_limit, neighbors: dict):
    current_path = start_path[0]
    best_path = current_path
    tabu_list = list()
    tabu_list.append(current_path)

    global_start = time.time()
    while time.time() - global_start <= time_limit:
        r = shake_path(deepcopy(current_path))
        for _ in range(num_of_shakes):
            if time.time() - global_start > time_limit:
                break
            w = shake_path(deepcopy(current_path))
            if w not in tabu_list and (r in tabu_list or calculate_cost(w, neighbors) < calculate_cost(r, neighbors)):
                r = w
        if r not in tabu_list:
            current_path = r
            tabu_list.append(r)
        current_cost = calculate_cost(current_path, neighbors)
        best_cost = calculate_cost(best_path, neighbors)
        if current_cost < best_cost:
            print("new best", current_cost, "prev", best_cost, file=sys.stderr)
            best_path = current_path
            best_cost = current_cost
        if len(tabu_list) >= tabu_length:
            tabu_list.pop(0)
    return best_path, best_cost


t, n = map(int, input().split())
data = [[0]]
for x in [[*map(int, input().split())] for i in range(n)]:
    data.append(x)
nbs = neighbors_from_data(data)

bp, c = tabu_search(default_path(nbs), n*10, int(n**2/3), t, nbs)
print(c)
print(*bp, file=sys.stderr)
