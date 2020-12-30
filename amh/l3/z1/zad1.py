import time
import random

population_size = 8


def yang(x, epsilons):
    return sum(e_i * abs(x_i)**i for i, (x_i, e_i) in enumerate(zip(x, epsilons), 1))


def mate(first_parent, second_parent):
    first_offspring = first_parent.copy()
    second_offspring = second_parent.copy()

    left_pivot = random.randrange(len(first_offspring))
    right_pivot = random.randrange(len(second_offspring))
    if left_pivot > right_pivot:
        left_pivot, right_pivot = right_pivot, left_pivot

    for i in range(left_pivot, right_pivot):
        first_offspring[i], second_offspring[i] = second_offspring[i], first_offspring[i]

    return [first_offspring, second_offspring]


def mutate(individual):
    return [gene * random.gauss(1, 0.1) for i, gene in enumerate(individual)]


def selection(fitness_list):
    p_size = len(fitness_list)

    selected = random.randrange(p_size)

    for i in range(1, 4):
        rand_index = random.randrange(p_size)
        if fitness_list[rand_index] < fitness_list[selected]:
            selected = rand_index

    return selected


def genetic_algorithm(time_limit, x_vec, fitness_function):
    population = []

    for _ in range(population_size):
        population.append(mutate(x_vec))

    best_individual = None
    best_fitness = 10000000000000

    start_time = time.time()

    while time.time() - start_time < time_limit:
        fitness_list = []
        for individual in population:
            current_fitness = fitness_function(individual)
            fitness_list.append(current_fitness)

            if best_individual is None or current_fitness < best_fitness:
                best_individual = individual
                best_fitness = current_fitness

        next_generation = []

        for _ in range(population_size // 2):
            first_parent = population[selection(fitness_list)]
            second_parent = population[selection(fitness_list)]

            offsprings = mate(first_parent, second_parent)

            next_generation.append(mutate(offsprings[0]))
            next_generation.append(mutate(offsprings[1]))

        population = next_generation

    return best_individual, best_fitness


data = input().split()
t = int(data[0])
x_vector = list(map(float, data[1:6]))
epsilons = list(map(float, data[6:11]))

best_infividual, best_fitness = genetic_algorithm(t, x_vector, lambda x: yang(x, epsilons))
print(*best_infividual, best_fitness)
