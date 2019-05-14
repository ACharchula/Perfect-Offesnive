import random

from deap import base
from deap import creator
from deap import tools

from structures import *

data = AllData.load_data_from_file("przestrzen.txt")

#function used to generate random indices of class Player
def create_player():
    return Player(random.randint(64, 99), random.randint(64, 99), random.randint(64, 99))


creator.create("FitnessMax", base.Fitness, weights=(1.0,)) #weights is 1.0 because we want to maximize it
creator.create("Individual", list, fitness=creator.FitnessMax) #our individual(chromosome) is a list of 3 players
#during crossover we will cross two individuals and if one doesn't exist in the search space then it's score will be 0

toolbox = base.Toolbox()
#define one gene (index) to be a player returned by create_player method
toolbox.register("indices", create_player)
#define individual to call indices function (create_player) 3 times
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.indices, n=3)

ind = toolbox.individual()  # [ Player1, Player2, Player3 ]

print(ind[0])
print("\n")
print(ind[1])
print("\n")
print(ind[2])
print("\n")

