from copy import deepcopy

import numpy as np

chromosomes = np.random.choice([True, False], 1000)


def mutate(mutation_rate, mutation_range=0):
    for index in range(len(chromosomes)):
        if np.random.uniform() < mutation_rate:
            chromosomes[index] = True if chromosomes[index] is False else False


original_chromosomes = deepcopy(chromosomes)
mutate(0.2)

differences = []

for i in range(len(chromosomes)):
    if chromosomes[i] != original_chromosomes[i]:
        differences.append(chromosomes[i])

print(differences)
print(len(differences))
