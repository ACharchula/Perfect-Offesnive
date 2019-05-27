from simanneal import Annealer
import time

import random

class SimulatedAnnealing(Annealer):

    def __init__(self, state, data):
        self.data = data
        self.state = state
        super(SimulatedAnnealing, self).__init__(self.state)

    def move(self):
        key = random.choice(self.data.players_and_scores[self.state].neighbours)
        self.state = key

    def energy(self):
        score = self.data.players_and_scores[self.state].score
        if score == 13:
            self.steps = 0
        return 20 - score
        # 20 is a random number, the state will change if energy decrease


def perform_simulated_annealing(start_key, data, steps):
    sa = SimulatedAnnealing(start_key, data)
    sa.steps = steps
    sa.copy_strategy = "slice"
    print('===Simulated Annealing===')
    start = time.time()
    state, e = sa.anneal()
    end = time.time()
    print("Time =" + (end - start).__str__() )
    print(data.players_and_scores[state].player1)
    print(data.players_and_scores[state].player2)
    print(data.players_and_scores[state].player3)
    print(data.players_and_scores[state].score)
    print('=========================')
