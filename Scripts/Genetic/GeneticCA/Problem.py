from Genetic.GeneticCA.Utils import cost


class Problem:
    number_of_genes: int
    max_val: int
    min_val: int

    def __init__(self, number_of_genes=16):
        self.number_of_genes = number_of_genes
        self.max_val = number_of_genes
        self.min_val = 1
        self.cost = cost
