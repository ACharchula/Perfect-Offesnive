from simanneal import Annealer
import random
from src.structures import *


class SimulatedAnnealing(Annealer):

    def __init__(self, state, data):
        self.data = data
        self.state = state
        super(SimulatedAnnealing, self).__init__(self.state)

    def move(self):
        key = random.choice(self.state.neighbours)
        self.state = self.data.players_and_scores[key]

    def energy(self):
        score = self.state.score
        return 20 - score
        # 20 is a random number, the state will change if energy decrease


def perform_simulated_annealing(start_key, players_and_scores, steps):
    data = AllData(players_and_scores)
    data.assign_neighbours()
    sa = SimulatedAnnealing(data.players_and_scores[start_key], data)
    sa.steps = steps
    print('===Simulated Annealing===')
    state, e = sa.anneal()

    print(state.player1)
    print(state.player2)
    print(state.player3)
    print(state.score)
    print('=========================')
