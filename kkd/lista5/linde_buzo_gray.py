from collections import defaultdict
from functools import reduce
from math import floor
from math import fabs
from util import squared_euclid_distance


def prepare_code_book(b_map, limit, eps=0.00001):
    c_book = []

    initial_code_vector = average_vector(b_map)
    c_book.append(initial_code_vector)

    avg_distortion = initial_distortion(initial_code_vector, b_map)

    while len(c_book) < limit:
        c_book, avg_distortion = split_code_book(b_map, c_book, eps, avg_distortion)

    return [(floor(b), floor(g), floor(r)) for b, g, r in c_book]


def split_code_book(b_map, c_book, eps, distortion):

    new_code_vectors = []
    for code_vector in c_book:
        cv_1 = shake_code_vector(code_vector, eps)
        cv_2 = shake_code_vector(code_vector, -eps)
        new_code_vectors.extend((cv_1, cv_2))

    c_book = new_code_vectors

    print("Splitting", len(c_book))

    avg_distortion = 0
    error = eps + 1
    while error > eps:
        nearest_code_vectors = [None] * len(b_map)
        input_vectors_near_code_vector = defaultdict(list)
        input_vector_indexes_near_code_vector = defaultdict(list)
        for i, input_vec in enumerate(b_map):
            min_distance = None
            closest_c_index = None
            for cv_index, code_vector in enumerate(c_book):
                distance = squared_euclid_distance(input_vec, code_vector)
                if min_distance is None or distance < min_distance:
                    min_distance = distance
                    nearest_code_vectors[i] = code_vector
                    closest_c_index = cv_index
            input_vectors_near_code_vector[closest_c_index].append(input_vec)
            input_vector_indexes_near_code_vector[closest_c_index].append(i)

        for cv_index in range(len(c_book)):
            vectors = input_vectors_near_code_vector.get(cv_index) or []
            if len(vectors) > 0:
                new_center_vector = average_vector(vectors)
                c_book[cv_index] = new_center_vector
                for i in input_vector_indexes_near_code_vector[cv_index]:
                    nearest_code_vectors[i] = new_center_vector

        prev_avg_distortion = avg_distortion if avg_distortion > 0 else distortion
        avg_distortion = average_distortion(nearest_code_vectors, b_map)

        error = (avg_distortion - prev_avg_distortion) / avg_distortion
        error = fabs(error)

    return c_book, avg_distortion


def initial_distortion(initial_code_vector, b_map):
    return reduce(lambda s, d: s + d / len(b_map), (squared_euclid_distance(initial_code_vector, input_vector) for input_vector in b_map), 0.0)


def average_distortion(code_list, b_map):
    return reduce(lambda s, d: s + d / len(b_map), (squared_euclid_distance(c, b_map[i]) for i, c in enumerate(code_list)), 0.0)


def shake_code_vector(code, eps):
    return [x * (1.0 + eps) for x in code]


def average_vector(vectors: list):
    result = [0.0, 0.0, 0.0]
    for vector in vectors:
        for i, x in enumerate(vector):
            result[i] += x / len(vectors)

    return result
