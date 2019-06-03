from simanneal import Annealer
import time

import random

class SimulatedAnnealing(Annealer):

    def __init__(self, state, data, value_to_find, max_price):
        self.data = data
        self.value_to_find = value_to_find
        self.state = state
        self.max_price = max_price
        super(SimulatedAnnealing, self).__init__(self.state)

    def move(self):
        key = random.choice(self.data.players_and_scores[self.state].neighbours)
        self.state = key

    def energy(self):
        score = self.data.players_and_scores[self.state].score

        cost = (int(self.state[0]) + int(self.state[3]) + int(self.state[6]))/3
        if cost > self.max_price:
            return cost

        if score == self.value_to_find:
            self.steps = 0
            return 0

        return 20 - score
        # 20 is a random number, the state will change if energy decrease


def perform_simulated_annealing(start_key, data, steps, value_to_find, max_price):
    sa = SimulatedAnnealing(start_key, data, value_to_find, max_price)
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

def perform_simulated_annealing_test(start_key, data, steps, value_to_find, max_price, Tmax, Tmin):
    sa = SimulatedAnnealing(start_key, data, value_to_find, max_price)
    sa.steps = steps

    if Tmax != -1:
        sa.Tmax = Tmax

    if Tmin != -1:
        sa.Tmin = Tmin

    sa.updates = 0
    sa.copy_strategy = "slice"
    start = time.time()
    state, e = sa.anneal()
    end = time.time()
    return end - start, data.players_and_scores[state].score
