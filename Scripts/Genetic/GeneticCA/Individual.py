from copy import deepcopy
from typing import List

import numpy as np


class Individual:
    chromosome: List[int]
    cost: int

    def __init__(self, problem):
        self.chromosome = [i for i in range(1, problem.number_of_genes + 1)]
        np.random.shuffle(self.chromosome)
        self.cost = problem.cost(self.chromosome)

    def mutate(self, rate_of_gene_mutation: float, range_of_gene_mutation: float = 0):
        for index in range(len(self.chromosome)):
            if np.random.uniform() < rate_of_gene_mutation:
                index1, index2 = np.random.choice(len(self.chromosome), 2)
                (self.chromosome[index1], self.chromosome[index2]) = (self.chromosome[index2], self.chromosome[index1])

    def crossover(self, other_individual, explore_crossover: int = 0):
        child1 = deepcopy(self)
        child2 = deepcopy(other_individual)

        index1, index2 = 0, 0
        while index1 == index2:
            index1, index2 = sorted(np.random.choice(len(self.chromosome), size=2))

        child1_chromosome = self.chromosome[index1:index2]
        child1.chromosome = [x for x in other_individual.chromosome if x not in child1_chromosome]
        child1.chromosome = child1.chromosome[:index1] + child1_chromosome + child1.chromosome[index1:]

        index1, index2 = 0, 0
        while index1 == index2:
            index1, index2 = sorted(np.random.choice(len(other_individual.chromosome), size=2))

        child2_chromosome = other_individual.chromosome[index1:index2]
        child2.chromosome = [x for x in self.chromosome if x not in child2_chromosome]
        child2.chromosome = child2.chromosome[:index1] + child2_chromosome + child2.chromosome[index1:]

        return child1, child2
