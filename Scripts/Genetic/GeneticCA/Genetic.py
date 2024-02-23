from copy import deepcopy

import numpy as np

from Genetic.GeneticCA.Individual import Individual
from Genetic.GeneticCA.Parameters import Parameters
from Genetic.GeneticCA.Problem import Problem


def main():
    problem = Problem(25)
    parameters = Parameters()

    best_individual: Individual = run_genetic(problem, parameters)
    # individual1 = Individual(problem)
    # individual2 = Individual(problem)
    #
    # individual1.chromosome = [5, 6, 8, 2, 3, 9, 4, 1, 7]
    # individual2.chromosome = [1, 7, 2, 6, 3, 9, 8, 4, 5]
    #
    # child1, child2 = individual1.crossover(individual2)
    # print(child1.chromosome)
    # print(child2.chromosome)


def choose_indices_from(number_in_list: int):
    index1 = np.random.randint(number_in_list)
    index2 = np.random.randint(number_in_list)

    if index1 == index2:
        return choose_indices_from(number_in_list)

    return index1, index2


def run_genetic(problem, parameters):
    cost = problem.cost
    number_in_population = parameters.population
    max_number_of_generations = parameters.max_number_of_generations
    number_of_children_per_generation = parameters.child_rate_per_generation * number_in_population
    explore_crossover = parameters.crossover_explore_rate
    rate_of_gene_mutation = parameters.rate_of_gene_mutation
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
            parent_index1, parent_index2 = choose_indices_from(len(population))

            parent1 = population[parent_index1]
            parent2 = population[parent_index2]

            child1, child2 = parent1.crossover(parent2, explore_crossover)
            child1.mutate(rate_of_gene_mutation)
            child2.mutate(rate_of_gene_mutation)

            child1.cost = cost(child1.chromosome)
            child2.cost = cost(child2.chromosome)

            children.append(child1)
            children.append(child2)

            population += children

            population = sorted(population, key=lambda x: x.cost)
            population = population[:number_in_population]

            if population[0].cost < best_solution.cost:
                best_solution = population[0]

        print(
            f'Best Solution for Generation {i + 1} is:\nCost: {best_solution.cost} \nChromosomes: '
            f'{best_solution.chromosome}')

        if best_solution.cost == 0:
            break

    print(
        f'Best Solution Found is:\nCost: {best_solution.cost} \nChromosomes: {best_solution.chromosome}')

    return best_solution


if __name__ == '__main__':
    main()
