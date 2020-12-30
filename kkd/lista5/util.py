def squared_euclid_distance(a, b):
    return sum((x_a - x_b) ** 2 for x_a, x_b in zip(a, b))


def mean_square_error(data1, data2):
    return (1 / len(data1)) * sum([squared_euclid_distance(data1[i], data2[i]) ** 2 for i in range(len(data1))])


def signal_noise_ratio(x, mse):
    return ((1 / len(x)) * sum(sum(x_i_j**2 for x_i_j in x_i) for x_i in x)) / mse


def get_index(data, x) -> int:
    for i, d in enumerate(data):
        if d == x:
            return i
    return -1
