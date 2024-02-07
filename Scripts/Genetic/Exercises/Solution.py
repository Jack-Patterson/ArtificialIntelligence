from copy import deepcopy

import numpy as np

from Genetic.Individual import Individual
from Genetic.Parameters import Parameters
from Genetic.Problem import Problem


def main():
    # problem_for_exercise = Problem()
    # problem_for_exercise.number_of_genes = 5
    # problem_for_exercise.cost = cost_function_for_exercise
    # parameters = Parameters()
    #
    # print(cost_function_for_exercise([1, 2, 3, 4, 5]))
    # best_solution = run_genetic(problem_for_exercise, parameters)
    #
    # prob_lp = Problem
    # prob_lp.number_of_genes = 5
    # prob_lp.cost = cost_lp
    # prob_lp.min_val = 0
    # prob_lp.max_val = 10

    # to complete

    problem = Problem()
    problem.number_of_genes = 10
    problem.min_val = 1
    problem.max_val = 10
    problem.cost = cost_for_individual

#cost = if weight > total weight return infinity else weight

    weights = np.random.uniform(1, 10, 1000)
    print(weights)

    individual = Individual(problem)
    individual.chromosome_weight = np.random.choice(weights, problem.number_of_genes)
    individual.cost = problem.cost(individual.chromosome_weight)
    print(individual.chromosome_weight)
    print(individual.cost)

    # https://colab.research.google.com/drive/1TJTnsK1GNkdkB-TDtovrT0FzOPaKV8iZ?usp=sharing#scrollTo=iJt94QdfKwXJ

    values = np.random.randint(0, 50, 1000)
    individual.chromosome_value = np.random.choice(values, problem.number_of_genes)
    individual.cost = problem.cost(individual.chromosome_weight)
    print(individual.chromosome_value)
    print(individual.cost)


def cost_for_individual(x):

    return sum(x)


def cost_lp(v):
    if v[1] + v[2] + v[3] < 10:
        return 1000000000


def cost_function_for_exercise(x):
    return (x[0] - 1) ** 2 + (x[1] - 2) ** 2 + (x[2] - 3) ** 2 + (x[3] - 4) ** 2 + (x[4] - 5) ** 2


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
            parent_index1, parent_index2 = choose_indices_from(len(population))

            parent1 = population[parent_index1]
            parent2 = population[parent_index2]

            child1, child2 = parent1.crossover(parent2, explore_crossover)
            child1.mutate(rate_of_gene_mutation, range_of_gene_mutation)
            child2.mutate(rate_of_gene_mutation, range_of_gene_mutation)

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
                f'Best Solution for Generation {i} is:\nCost: {best_solution.cost} \nChromosomes: '
                f'{best_solution.chromosome}')

    return best_solution


if __name__ == "__main__":
    main()
