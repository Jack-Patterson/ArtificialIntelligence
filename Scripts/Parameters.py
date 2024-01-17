class Parameters:
    population: int
    max_number_of_generations: int
    child_rate_per_generation: float
    crossover_explore_rate: float
    rate_of_gene_mutation: float
    range_of_gene_mutation: float

    def __init__(self):
        self.population = 1000
        self.max_number_of_generations = 100
        self.child_rate_per_generation = 1
        self.crossover_explore_rate = 0.2
        self.rate_of_gene_mutation = 0.2
        self.range_of_gene_mutation = 0.5
