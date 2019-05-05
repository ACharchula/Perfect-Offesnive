from simanneal import Annealer
import random

class SimulatedAnnealing(Annealer):

    def __init__(self, players_and_scores):
        self.players_and_scores = players_and_scores
        self.state = players_and_scores[0]
        super(SimulatedAnnealing, self).__init__(self.state)

    def move(self):
        player = random.randint(0, 2)
        #EHHHH...

    def energy(self):
        score = self.state[len(self.state)-1]
        return 20 - score
        #20 is a random number, the state will change if energy decrease


class Player:

    def __init__(self, overall, shot, finishing):
        self.overall = overall
        self.shot = shot
        self.finishing = finishing

    #def find_neighbour(self, players_and_scores):
