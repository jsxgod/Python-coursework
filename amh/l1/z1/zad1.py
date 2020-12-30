import random
import time
import math


def norm(vector):
    return math.sqrt(sum(x ** 2 for x in vector))


def happy_cat(vector):
    return ((norm(vector) ** 2 - 4) ** 2) ** 1 / 8 + 1 / 4 * (1 / 2 * norm(vector) ** 2 + sum(vector)) + 1 / 2


def griewank(vector):
    return 1.0 + sum(((xi ** 2) / 4000.0) for xi in vector) \
           - math.prod((math.cos(xi / (i + 1.0)) for i, xi in enumerate(vector)))


def random_vector(vector_size):
    return tuple(random.gauss(0, 1) for _ in range(vector_size))


def search_neighbor(vector):
    return tuple(xi + random.gauss(0, 0.0001) for xi in vector)


def shake(vector):
    return tuple(xi + random.gauss(0, 0.000001) for xi in vector)


def local_search(vector_size, f, time_limit):
    current = random_vector(vector_size)
    best = current
    home_base = current

    global_start = time.time()
    while time.time() - global_start < time_limit:

        # LOCAL SEARCH that improves the current solution
        local_time = time.time()
        while time.time() - local_time < 1 / 100 and time.time() - global_start < time_limit:
            neighbour = search_neighbor(current)
            if f(neighbour) < f(current):
                current = neighbour

        # REMEMBER TO SAVE THE BEST SOLUTION SO FAR
        if f(current) <= f(best):
            best = current

        # SAVE "INFORMATION" ABOUT CURRENT REGION
        # IF BETTER THAN THE PREVIOUS HOME BASE
        if f(current) <= f(home_base):
            home_base = current

        current = shake(home_base)

    return best, f(best)


t, b = map(int, input().split())

if b == 0:
    print(local_search(4, happy_cat, t))
else:
    print(local_search(4, griewank, t))
