from copy import deepcopy, copy

import numpy as np

from Individual import Individual
from Parameters import Parameters
from Problem import Problem


def main():
    rate_of_gene_mutation: float = 0.25
    range_of_gene_mutation: float = 2

    problem1: Problem = Problem()
    problem2: Problem = Problem()
    individual1: Individual = Individual(problem1)
    individual2: Individual = Individual(problem2)

    individual1_initial_chromosome = copy(individual1.chromosome)
    individual1.mutate(rate_of_gene_mutation, range_of_gene_mutation)
    print(f'Individual 1: \nChromosome: {individual1_initial_chromosome} \nCost: {individual1.cost} \n'
          f'Mutated Chromosome: {individual1.chromosome}')

    individual2_initial_chromosome = copy(individual2.chromosome)
    individual2.mutate(rate_of_gene_mutation, range_of_gene_mutation)
    print(f'Individual 2: \nChromosome: {individual2_initial_chromosome} \nCost: {individual2.cost} \n'
          f'Mutated Chromosome: {individual2.chromosome}')

    child1, child2 = individual1.crossover(individual2, .5)
    print(child1.chromosome)
    print(child2.chromosome)

    parameter1 = Parameters()

    best_individual = run_genetic(problem1, parameter1)
    print(best_individual.cost)
    print(best_individual.chromosome)


def choose_indices_from(number_in_list: int):
    index1 = np.random.randint(number_in_list)
    index2 = np.random.randint(number_in_list)

    if index1 == index2:
        return choose_indices_from(number_in_list)

    return index1, index2


def run_genetic(problem: Problem, parameters: Parameters):
    cost = problem.cost
    number_in_population = parameters.population
    max_number_of_generations = parameters.max_number_of_generations
    number_of_children_per_generation = parameters.child_rate_per_generation * number_in_population
    explore_crossover = parameters.crossover_explore_rate
    rate_of_gene_mutation = parameters.rate_of_gene_mutation
    range_of_gene_mutation = parameters.range_of_gene_mutation
    population = []

    best_solution = Individual(problem)
    best_solution.cost = np.Inf

    for i in range(number_in_population):
        individual = Individual(problem)
        population.append(individual)

        if individual.cost < best_solution.cost:
            best_solution = deepcopy(individual)

    for i in range(max_number_of_generations):
        children = []

        while len(children) < number_of_children_per_generation:
            parent_index1, parent_index2 = choose_indices_from(population)

            parent1 = population[parent_index1]
            parent2 = population[parent_index2]

            child1, child2 = parent1.crossover(parent2, explore_crossover)
            child1.mutate(rate_of_gene_mutation, range_of_gene_mutation)
            child2.mutate(rate_of_gene_mutation, range_of_gene_mutation)

            child1.cost = cost(child1.chromosome)
            child2.cost = cost(child2.chromosome)

            children.append(child1)
            children.append(child2)



    return best_solution


if __name__ == "__main__":
    main()
