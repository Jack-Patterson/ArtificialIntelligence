from copy import deepcopy
from typing import List

import numpy as np

from Problem import Problem


class Individual:
    chromosome: List[float]
    cost: int

    def __init__(self, problem: Problem):
        self.chromosome = np.random.uniform(problem.min_val, problem.max_val, problem.number_of_genes)
        self.cost = problem.cost(self.chromosome)

    def mutate(self, rate_of_gene_mutation: float, range_of_gene_mutation: float):
        for index in range(len(self.chromosome)):
            if np.random.uniform() < rate_of_gene_mutation:
                self.chromosome[index] += np.random.randn() * range_of_gene_mutation

    def crossover(self, other_individual, explore_crossover: int):
        alpha = np.random.uniform(-explore_crossover, 1 + explore_crossover)

        child1 = deepcopy(self)
        child2 = deepcopy(other_individual)

        child1.chromosome = alpha * self.chromosome + (1 - alpha) * other_individual.chromosome
        child2.chromosome = alpha * other_individual.chromosome + (1 - alpha) * self.chromosome

        return child1, child2
