import random

from deap import base
from deap import creator
from deap import tools

from structures import *

data = AllData.load_data_from_file("przestrzen.txt")


def create_player():
    return Player(random.randint(64, 99), random.randint(64, 99), random.randint(64, 99))


creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("indices", create_player)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.indices, n=3)

ind = toolbox.individual()

print(ind[0])
print("\n")
print(ind[1])
print("\n")
print(ind[2])
print("\n")

