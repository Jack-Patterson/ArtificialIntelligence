import copy

from Individual import Individual
from Problem import Problem


def main():
    rate_of_gene_mutation: float = 0.25
    range_of_gene_mutation: float = 2

    problem1: Problem = Problem()
    problem2: Problem = Problem()
    individual1: Individual = Individual(problem1)
    individual2: Individual = Individual(problem2)

    individual1_initial_chromosome = copy.copy(individual1.chromosome)
    individual1.mutate(rate_of_gene_mutation, range_of_gene_mutation)
    print(f'Individual 1: \nChromosome: {individual1_initial_chromosome} \nCost: {individual1.cost} \n'
          f'Mutated Chromosome: {individual1.chromosome}')

    individual2_initial_chromosome = copy.copy(individual2.chromosome)
    individual2.mutate(rate_of_gene_mutation, range_of_gene_mutation)
    print(f'Individual 2: \nChromosome: {individual2_initial_chromosome} \nCost: {individual2.cost} \n'
          f'Mutated Chromosome: {individual2.chromosome}')


if __name__ == "__main__":
    main()
