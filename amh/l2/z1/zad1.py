import sys
from random import gauss

import numpy as np
import numpy.random as rn
import math
import time


interval = (-100, 100)


def norm(vector):
    return math.sqrt(sum(x ** 2 for x in vector))


def salomon(vector):
    return 1 - math.cos(2*math.pi * norm(vector)) + 0.1 * norm(vector)


def clip(x):
    a, b = interval
    return max(min(x, b), a)


def random_start():
    a, b = interval
    vector = []
    for _ in range(4):
        vector.append(a + (b - a) * rn.random_sample())
    return [clip(x) for x in vector]


def cost_function(x):
    return salomon(x)


def random_neighbour(state):
    return [clip(x * gauss(1, 0.1)) for x in state]


def random_neighbour2(vector, fraction=1):
    amplitude = (max(interval) - min(interval)) * fraction / 10
    deltas = [(-amplitude/2.) + amplitude * x for x in list(rn.random(len(vector)))]
    return [clip(x + delta) for x, delta in zip(vector, deltas)]


def acceptance_probability(cost, new_cost, temperature):
    if new_cost <= cost:
        return 1
    else:
        p = np.exp((cost - new_cost) / temperature)
        return p


def temperature(fraction):
    return max(0.01, min(1, 1 - fraction))


def annealing(start_state,
              cost_function,
              random_neighbour,
              acceptance,
              temperature,
              time_limit=5):
    state = start_state
    cost = cost_function(state)
    states, costs = [state], [cost]

    start_time = time.time()
    time_delta = time.time() - start_time

    while time_delta < time_limit:
        fraction = time_delta / float(time_limit)
        T = temperature(fraction)
        new_state = random_neighbour(state)
        new_cost = cost_function(new_state)

        if acceptance(cost, new_cost, T) > rn.random():
            state, cost = new_state, new_cost
            states.append(state)
            costs.append(cost)
        time_delta = time.time() - start_time
    return state, cost_function(state), states, costs


t, x1, x2, x3, x4 = map(float, input().split())
# state, c, states, costs = annealing(random_start, salomon, random_neighbour, acceptance_probability, temperature, time_limit=t)
state, c, states, costs = annealing([x1, x2, x3, x4], salomon, random_neighbour, acceptance_probability, temperature, time_limit=t)
print(*state, file=sys.stderr)
print(c)
