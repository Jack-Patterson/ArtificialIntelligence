import numpy as np
from typing import List

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
