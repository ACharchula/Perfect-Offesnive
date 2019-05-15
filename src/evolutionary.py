import random

from deap import base
from deap import creator
from deap import tools

from src.structures import *

data = AllData.load_data_from_file("przestrzen.txt")

plrs = ('85', '87', '85', '78', '80', '81', '69', '67', '70')
print(plrs[6:10])
print(plrs[:6])


# function used to generate random indices of class Player
def create_player():
    # return Player(random.randint(64, 99), random.randint(64, 99), random.randint(64, 99))
    return random.randint(64, 99).__str__(), random.randint(64, 99).__str__(), random.randint(64, 99).__str__()


def evaluate(individual):
    return data.get_score(individual),


# crossover is about swapping last players of two threes
def cross_over(individual1, individual2):
    return individual1[:6] + individual2[6:10], individual2[:6] + individual1[6:10]


# we randomly choose if we mutate or not. If we do we randomly pick a neighbor (if one exists) of the individual
def mutate(individual):
    if random.uniform(0, 1) < 0.1:
        return data.get_random_neighbor(individual)
    return individual


def init_individual():
    return create_player() + create_player() + create_player()


creator.create("FitnessMax", base.Fitness, weights=(1.0,))  # weights is 1.0 because we want to maximize it
creator.create("Individual", tuple, fitness=creator.FitnessMax)  # our individual(chromosome) is a list of 3 players
# during crossover we will cross two individuals and if one doesn't exist in the search space then it's score will be 0

toolbox = base.Toolbox()
# define one gene (index) to be a player returned by create_player method
toolbox.register("indices", create_player)
# define individual to call indices function (create_player) 3 times
toolbox.register("individual", init_individual)

toolbox.register("evaluate", evaluate)
toolbox.register("mate", cross_over)
toolbox.register("mutate", mutate)
toolbox.register("select", tools.selTournament, tournsize=3)

# defines a population to be a list of individuals
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# ind1 = toolbox.individual()  # [ Player1, Player2, Player3 ]
# ind2 = toolbox.individual()  # [ Player1, Player2, Player3 ]
# # ind.fitness.values = evaluate(ind)
# print(ind1)
# print(ind2)
#
# print("------------------")
# crosoverd = toolbox.mate(ind1, ind2)
# for ind in crosoverd:
#     print(ind)
#
# print("------------------")
#
# mutated = toolbox.mutate(plrs)
# print(mutated)


# initializes our population with 100 individuals
pop = toolbox.population(n=100)
