from deap import base
from deap import creator
from deap import tools

from src.structures import *

data = AllData.load_data_from_file("przestrzen2.txt")


def evaluate(individual, max_price):
    score = data.get_score(individual)
    cost = (int(individual[0]) + int(individual[3]) + int(individual[6])) / 3
    if cost < max_price:
        return score,

    return 0.0,
    # return data.get_score(individual),


# crossover is about swapping last players of two threes
def cross_over(individual1, individual2):
    return creator.Individual(individual1[:6] + individual2[6:10]), creator.Individual(
        individual2[:6] + individual1[6:10])


# we randomly choose if we mutate or not. If we do we randomly pick a neighbor (if one exists) of the individual
def mutate(individual):
    return creator.Individual(data.get_random_neighbor(individual))


def init_individual(ind_class):
    return ind_class(data.get_random_players())
    # return ind_class(create_player() + create_player() + create_player())


creator.create("FitnessMax", base.Fitness, weights=(1.0,))  # weights is 1.0 because we want to maximize it
creator.create("Individual", tuple, fitness=creator.FitnessMax)  # our individual(chromosome) is a list of 3 players
# during crossover we will cross two individuals and if one doesn't exist in the search space then it's score will be 0

toolbox = base.Toolbox()
# define one gene (index) to be a player returned by create_player method
# toolbox.register("indices", create_player)
# define individual to call indices function (create_player) 3 times
toolbox.register("individual", init_individual, creator.Individual)

toolbox.register("evaluate", evaluate)
toolbox.register("mate", cross_over)
toolbox.register("mutate", mutate)
toolbox.register("select", tools.selBest)

# defines a population to be a list of individuals
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def run_evolutionary_algorithm(crossover_possibility, mutation_possibility, population_size, max_price, max_stagnation, wanted_value):
    pop = toolbox.population(n=population_size)

    for ind in pop:
        ind.fitness.values = toolbox.evaluate(ind, max_price)

    CXPB = crossover_possibility
    MUTPB = mutation_possibility

    g = 0
    didnt_change = 0
    curr_best = tools.selBest(pop, 1)[0]
    fits = [ind.fitness.values[0] for ind in pop]
    if wanted_value is None:
        wanted_value = -1


    while didnt_change < max_stagnation:# and max(fits) >= wanted_value:
        g = g + 1
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        # offspring = list(map(toolbox.clone, offspring))

        for i in range(0, len(offspring) - 1, 2):
            if random.random() < CXPB:
                offspring[i], offspring[i + 1] = toolbox.mate(offspring[i], offspring[i + 1])

        for i in range(len(offspring)):
            if random.random() < MUTPB:
                offspring[i] = toolbox.mutate(offspring[i])

        best_ind = tools.selBest(pop, 1)[0]
        # we make sure to take the best element from previous population to the next population
        pop = toolbox.select([best_ind] + offspring, len(pop))

        # increasing counter if the best element remains the same
        if best_ind == curr_best:
            didnt_change = didnt_change + 1
        else:
            didnt_change = 0
            curr_best = best_ind

        for ind in pop:
            ind.fitness.values = toolbox.evaluate(ind, max_price)

        fits = [ind.fitness.values[0] for ind in pop]

    best_ind = tools.selBest(pop, 1)[0]
    return g, best_ind, best_ind.fitness.values
