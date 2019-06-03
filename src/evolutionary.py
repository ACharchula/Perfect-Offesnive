from deap import base
from deap import creator
from deap import tools

from src.structures import *

data = AllData.load_data_from_file("przestrzen2.txt")

# function used to generate random indices of class Player
def create_player():
    # return Player(random.randint(64, 99), random.randint(64, 99), random.randint(64, 99))
    return random.randint(64, 99).__str__(), random.randint(64, 99).__str__(), random.randint(64, 99).__str__()


def evaluate(individual):
    return data.get_score(individual),  # individual[0] + individual[2] + individual[5]


# crossover is about swapping last players of two threes
def cross_over(individual1, individual2):
    individual1 = individual1[:6] + individual2[6:10]
    individual2 = individual2[:6] + individual1[6:10]
    return creator.Individual(individual1), creator.Individual(individual2)


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
toolbox.register("select", tools.selTournament, tournsize=20)

# defines a population to be a list of individuals
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def main():
    pop = toolbox.population(n=100)

    for ind in pop:
        ind.fitness.values = toolbox.evaluate(ind)

    fits = [ind.fitness.values[0] for ind in pop]

    print(fits)

    CXPB = 0.5
    MUTPB = 0.2

    g = 0
    while max(fits) < 13:
        g = g + 1
        # print("-- Generation %i --" % g)

        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        # offspring = list(map(toolbox.clone, offspring))
        offspring.sort(key=lambda x: toolbox.evaluate(x), reverse=True)

        for i in range(0, len(offspring) - 1, 2):
            if random.random() < CXPB:
                offspring[i], offspring[i + 1] = toolbox.mate(offspring[i], offspring[i + 1])

        for i in range(len(offspring)):
            if random.random() < MUTPB:
                offspring[i] = toolbox.mutate(offspring[i])

        # The population is entirely replaced by the offspring
        pop = toolbox.select(pop + offspring, len(pop))

        for ind in pop:
            ind.fitness.values = toolbox.evaluate(ind)

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x * x for x in fits)
        std = abs(sum2 / length - mean ** 2) ** 0.5

        # print("  Min %s" % min(fits))
        # print("  Max %s" % max(fits))
        # print("  Avg %s" % mean)
        # print("  Std %s" % std)
        #
        # print("-- End of (successful) evolution --")
        #
    best_ind = tools.selBest(pop, 1)[0]
    print("Generations %s" % (g));
    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))


if __name__ == "__main__":
    main()
