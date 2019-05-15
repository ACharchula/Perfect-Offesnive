from simanneal import Annealer
import time

import random

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


def perform_simulated_annealing(start_key, data, steps):
    sa = SimulatedAnnealing(data.players_and_scores[start_key], data)
    sa.steps = steps
    print('===Simulated Annealing===')
    start = time.time()
    state, e = sa.anneal()
    end = time.time()
    print("Time =" + (end - start).__str__() )
    print(state.player1)
    print(state.player2)
    print(state.player3)
    print(state.score)
    print('=========================')
