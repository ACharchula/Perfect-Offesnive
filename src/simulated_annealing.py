from simanneal import Annealer
import time

import random

class SimulatedAnnealing(Annealer):

    def __init__(self, state, data, value_to_find, max_price, stagnation):
        self.steps_counter = 0
        self.data = data
        self.stagnation = stagnation
        self.counter = 0
        self.previous_score = 1000
        self.value_to_find = value_to_find
        self.state = state
        self.last_key = state
        self.max_price = max_price
        super(SimulatedAnnealing, self).__init__(self.state)

    def move(self):
        key = random.choice(self.data.players_and_scores[self.state].neighbours)
        while key == self.last_key:
            key = random.choice(self.data.players_and_scores[self.state].neighbours)

        self.state = key
        self.last_key = key

    def energy(self):
        self.steps_counter += 1
        score = self.data.players_and_scores[self.state].score
        result = 0
        cost = (int(self.state[0]) + int(self.state[3]) + int(self.state[6]))/3
        if cost > self.max_price:
            result = cost

        if score == self.value_to_find:
            self.steps = 0
            return 0

        if result == 0:
            result = 20 - score

        if result <= self.previous_score:
            self.previous_score = result
            self.counter = 0
        else:
            self.counter += 1

        if self.counter == self.stagnation:
           self.steps = 0

        return result


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

def perform_simulated_annealing_test(start_key, data, steps, value_to_find, max_price, Tmax, Tmin, stagnation):
    sa = SimulatedAnnealing(start_key, data, value_to_find, max_price, stagnation)
    sa_auto = SimulatedAnnealing(start_key, data, value_to_find, max_price, stagnation)

    if Tmax == -1 or Tmin == -1:
        auto_schedule = sa_auto.auto(minutes=1)
        sa.Tmax = auto_schedule.get('tmax')
        sa.Tmin = auto_schedule.get('tmin')

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
    return end - start, data.players_and_scores[state].score, state, sa.Tmax, sa.Tmin, sa.steps_counter