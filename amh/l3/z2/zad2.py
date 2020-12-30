import time
import random
from collections import defaultdict, Counter
import sys

population_size = 8
num_of_elites = 4


def word_fitness(w):
    char_occurrences = Counter(w)

    for letter, occurrences in char_occurrences.items():
        if occurrences > global_character_occurrences[letter]:
            return 0

    if w in file_word_set:
        return sum(character_points_dict[c] for c in w)
    else:
        return 0


def mutate(w):
    char_occurrences = Counter(w)
    reduced_count = {c: global_character_occurrences[c] - char_occurrences[c] for c in global_character_occurrences}
    allowed_chars = [c for c, count in reduced_count.items() if count > 0]
    if not allowed_chars:
        return w

    random_char = random.choice(allowed_chars)
    random_index = random.randint(0, len(w))

    if random.random() > 0.1:
        w = w[:random_index] + random_char + w[random_index + 1:]
    else:
        w = w[:random_index] + random_char + w[random_index:]

    return w


def mate(first_parent, second_parent):
    first_offspring = list(first_parent)
    second_offspring = list(second_parent)

    min_length = min(len(first_parent), len(second_parent))

    for i in range(min_length):
        if random.random() < 0.1:
            first_offspring[i], second_offspring[i] = second_offspring[i], first_offspring[i]

    return [''.join(first_offspring), ''.join(second_offspring)]


def selection(fitness_list):
    selected = random.randrange(len(fitness_list))

    for i in range(1, 2):
        random_index = random.randrange(len(fitness_list))
        if fitness_list[random_index] > fitness_list[selected]:
            selected = random_index

    return selected


def remove_duplicates(data):
    no_duplicates = set()
    for c in data:
        no_duplicates.add(c)
    return list(no_duplicates)


def genetic_algroithm(time_limit, initial_population, fitness_function):
    population = initial_population

    best_individual = None
    best_fitness = 100000

    start_time = time.time()

    while time.time() - start_time < time_limit:
        fitness_list = []
        for individual in population:
            current_fitness = fitness_function(individual)
            fitness_list.append((individual, current_fitness))

            if best_individual is None or current_fitness > best_fitness:
                best_individual = individual
                best_fitness = current_fitness

        next_generation = []
        elite_individuals = remove_duplicates(map(lambda entry: entry[0], sorted(fitness_list, key=lambda entry: entry[1], reverse=True)))[:num_of_elites]
        for e in elite_individuals:
            next_generation.append(e)

        for _ in range((population_size - num_of_elites) // 2):
            first_parent = population[selection([fit[1] for fit in fitness_list])]
            second_parent = population[selection([fit[1] for fit in fitness_list])]

            offsprings = mate(first_parent, second_parent)

            next_generation += [mutate(offsprings[0]), mutate(offsprings[1])]

        population = next_generation

    return best_individual, best_fitness


with open('dict.txt') as f:
    file_word_set = set()
    for word in f.read().split():
        file_word_set.add(word)

t, n, s = [int(word) for word in input().split()]

character_points_dict = {}
global_character_occurrences = defaultdict(int)

for _ in range(n):
    c, point_value = input().split()
    character_points_dict[c] = int(point_value)
    global_character_occurrences[c] += 1

input_words = []
for _ in range(s):
    input_words.append(input().strip())

result_individual, result_fitness = genetic_algroithm(t, input_words, word_fitness)
print(result_fitness)
print(result_individual, file=sys.stderr)
