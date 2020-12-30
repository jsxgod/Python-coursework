import random
import sys
from math import floor
from typing import Union, Callable, Tuple

import numpy as np
import numpy.random as rn
import time

allowed_numbers = [0, 32, 64, 128, 160, 192, 223, 255]

t, n, m, k = map(int, input().split())
data = []
for _ in range(n):
    data.append([*map(np.uint8, input().split())])

col_intervals = [[] for _ in range(m)]


class Block:
    def __init__(self, row, col, length, height, value):
        self.anchor = (row, col)
        self.length = length
        self.height = height
        self.value = value


class Matrix:
    def __init__(self, n, m, blocks: list):
        self.height = n
        self.length = m
        self.blocks = blocks

    def __getitem__(self, point):
        r, col = point
        for block in self.blocks:
            if r in range(block.anchor[0], block.anchor[0] + block.height):
                if col in range(block.anchor[1], block.anchor[1] + block.length):
                    return block.value
        raise IndexError


def distance(m2: Matrix, m1=None):
    if m1 is None:
        m1 = data
    sum_result = 0
    for i in range(n):
        for j in range(m):
            sum_result += (m1[i][j] - m2[i, j]) ** 2
    return 1/(n*m) * sum_result


def check_col(c: int):
    result = 0
    for interval in col_intervals[c]:
        result += interval[1] - interval[0] + 1
    return result < n


def get_current_row(sorted_intervals):
    if len(sorted_intervals) == 1:
        if sorted_intervals[0][0] == 0:
            return sorted_intervals[0][1]+1, True
        else:
            return 0, False
    else:
        if sorted_intervals[0][0] == 0:
            for i in range(len(sorted_intervals[:-1])):
                if sorted_intervals[i][1] + 1 != sorted_intervals[i + 1][0]:
                    return sorted_intervals[i][1] + 1, False
            return sorted_intervals[-1][1] + 1, True
        else:
            return 0, False


def random_start2(n, m, k):
    blocks = []

    for col_index in range(m-k+1):
        current_row = 0
        while check_col(col_index):
            length = 0
            height = 0
            if not col_intervals[col_index]:
                height = rn.randint(k, n+1)
                length = rn.randint(k, (m - col_index) + 1)
                if col_index + length >= m - k:
                    length += m - col_index - length
                if height > n - k:
                    height = n

                block = Block(current_row, col_index, length, height, rn.choice(allowed_numbers))
                blocks.append(block)
                for c in range(col_index, col_index + length):
                    col_intervals[c].append((current_row, current_row+height-1))
            else:
                current_row, is_last = get_current_row(list(sorted(col_intervals[col_index], key=lambda x: x[0])))
                length = rn.randint(k, (m - col_index) + 1)
                if col_index + length >= m - k:
                    length += m - col_index - length

                if is_last:
                    height = rn.randint(k, (n - current_row) + 1)

                    if current_row <= n - k * 2:
                        if current_row + height >= n - k:
                            height += n - current_row - height
                        block = Block(current_row, col_index, length, height, rn.choice(allowed_numbers))
                        blocks.append(block)
                        for c in range(col_index, col_index + length):
                            col_intervals[c].append((current_row, current_row + height - 1))
                    else:
                        height = n - current_row
                        block = Block(current_row, col_index, length, height, rn.choice(allowed_numbers))
                        blocks.append(block)
                        for c in range(col_index, col_index + length):
                            col_intervals[c].append((current_row, current_row + height - 1))
                else:
                    next_interval_start = 0
                    for interval in col_intervals[col_index]:
                        if current_row < interval[0]:
                            next_interval_start = interval[0]
                            break

                    space = next_interval_start - current_row
                    if space < 2 * k:
                        block = Block(current_row, col_index, length, space, rn.choice(allowed_numbers))
                        blocks.append(block)
                        for c in range(col_index, col_index + length):
                            col_intervals[c].append((current_row, next_interval_start-1))
                    elif space >= 2 * k:
                        height = rn.randint(k, space + 1)
                        if current_row + height >= space - k:
                            height += space - current_row - height
                        block = Block(current_row, col_index, length, height, rn.choice(allowed_numbers))
                        blocks.append(block)
                        for c in range(col_index, col_index + length):
                            col_intervals[c].append((current_row, current_row + height - 1))

    return Matrix(n, m, blocks)


def random_start(n, m, k):
    blocks = []

    for i in range(n // k):
        for j in range(m // k):
            block = Block(i * k, j * k, k, k, rn.choice(allowed_numbers))
            blocks.append(block)

    if m % k != 0:
        for block in blocks:
            if block.anchor[1] == (m // k - 1) * k:
                block.length += m % k

    if n % k != 0:
        for block in blocks:
            if block.anchor[0] == (n // k - 1) * k:
                block.height += n % k

    return Matrix(n, m, blocks)


def change_random_block_value(matrix):
    block = random.choice(matrix.blocks)
    block.value = random.choice(allowed_numbers)
    return matrix


def blocks_values_swap(matrix):
    if len(matrix.blocks) > 1:
        first = random.choice(matrix.blocks)
        second = random.choice([b for b in matrix.blocks if b is not first])
        first.value, second.value = second.value, first.value
        return matrix
    else:
        return change_random_block_value(matrix)


def merge_and_split(matrix):
    def split(value):
        value1 = k
        value2 = k
        space = value - 2 * k
        while space > 0:
            if rn.random() > 0.5:
                value1 += 1
            else:
                value2 += 1
            space -= 1
        return value1, value2

    try:
        big_block = random.choice([b for b in matrix.blocks if b.height > k or b.length > k])
    except IndexError:
        return change_random_block_value(matrix)

    neighbour: Union[Block, None] = None
    direction: Union[str, None] = None

    for block in matrix.blocks:
        if block is big_block:
            continue
        if (
            block.anchor[0] == big_block.anchor[0]
            and block.height == big_block.height
            and (block.anchor[1] + block.length == big_block.anchor[1] or big_block.anchor[1] + big_block.length == block.anchor[1])
        ):
            neighbour, direction = block, "h"
            break

        if (
            block.anchor[1] == big_block.anchor[1]
            and block.length == big_block.length
            and (block.anchor[0] + block.height == big_block.anchor[0] or big_block.anchor[0] + big_block.height == block.anchor[0])
        ):
            neighbour, direction = block, "v"
            break

    if neighbour:
        if direction == "h":
            len1, len2 = split(big_block.length + neighbour.length)

            neighbour.anchor = (neighbour.anchor[0], min(big_block.anchor[1], neighbour.anchor[1]))
            neighbour.length = len1

            big_block.anchor = (neighbour.anchor[0], neighbour.anchor[1] + len1)
            big_block.length = len2
        else:
            height1, height2 = split(big_block.height + neighbour.height)

            neighbour.anchor = (min(big_block.anchor[0], neighbour.anchor[0]), neighbour.anchor[1])
            neighbour.height = height1

            big_block.anchor = (neighbour.anchor[0] + height1, neighbour.anchor[1])
            big_block.height = height2
    else:
        big_block.value = random.choice(allowed_numbers)

    return matrix


def choose_neighbour_function():
    return rn.choice([change_random_block_value, blocks_values_swap, merge_and_split])


def acceptance_probability(cost, new_cost, temperature):
    if new_cost <= cost:
        return 1
    else:
        p = np.exp((cost - new_cost) / temperature)
        return p


def temperature(fraction):
    return max(0.01, min(1, 1 - fraction))


def annealing(random_start, cost_function, random_neighbour, acceptance, temperature, time_limit=5):
    state = random_start(n, m, k + int(floor(k/4)))
    cost = cost_function(state)
    states, costs = [state], [cost]

    start_time = time.time()
    time_delta = time.time() - start_time

    while time_delta < time_limit:
        fraction = time_delta / float(time_limit)
        T = temperature(fraction)
        new_state = random_neighbour()(state)
        new_cost = cost_function(new_state)

        if acceptance(cost, new_cost, T) > np.random.random():
            state, cost = new_state, new_cost
            states.append(state)
            costs.append(cost)

        time_delta = time.time() - start_time
    return state, cost, states, costs


if n == m:
    rs = random_start
else:
    rs = random_start2
state, c, states, costs = annealing(rs, distance, choose_neighbour_function, acceptance_probability, temperature, time_limit=t)
str_result = ""
for i in range(state.height):
    current_row = []
    for j in range(state.length):
        current_row.append("{:3}".format(state[i, j]))
    str_result += " ".join(current_row) + "\n"
print(str_result, file=sys.stderr)
print(c)

