import pickle
import random


class Player:

    def __init__(self, overall, shot, finishing):
        self.overall = overall
        self.shot = shot
        self.finishing = finishing

    def __eq__(self, other):
        if int(other.overall) == int(self.overall) and int(other.shot) == int(self.shot) and int(
                other.finishing) == int(self.finishing):
            return True
        else:
            return False

    def __str__(self):
        return self.overall.__str__() + " " + self.shot.__str__() + " " + self.finishing.__str__()

    def get_stats(self):
        return [self.overall.__str__(), self.shot.__str__(), self.finishing.__str__()]


class PlayersAndScore:

    def __init__(self, key, value):
        self.player1 = Player(key[0], key[1], key[2])
        self.player2 = Player(key[3], key[4], key[5])
        self.player3 = Player(key[6], key[7], key[8])
        self.score = float(value)
        self.neighbours = list()

    def add_neighbour(self, neighbour):
        self.neighbours.append(neighbour)

    def check_if_contains_a_player(self, player):
        if player == self.player1 or player == self.player2 or player == self.player3:
            return True
        else:
            return False


class AllData:

    def __init__(self, players_scores):
        self.players_and_scores = dict()

        for k, v in players_scores.items():
            self.players_and_scores[k] = PlayersAndScore(k, v)

    def __contains__(self, players):
        return players in self.players_and_scores

    # neighbour is a row with at least one the same player among attackers

    def assign_neighbours(self):
        count = 0
        for k1, v1 in self.players_and_scores.items():
            print(count)
            for k2, v2 in self.players_and_scores.items():
                if k1 == k2:
                    continue

                if v2.check_if_contains_a_player(v1.player1) or v2.check_if_contains_a_player(
                        v1.player2) or v2.check_if_contains_a_player(v1.player3):
                    v1.add_neighbour(k2)

            count += 1

    def save_data_to_file(self, filename):
        file = open(filename, "wb")
        pickle.dump(self, file)
        file.close()

    def get_score(self, players_tuple):
        if players_tuple in self.players_and_scores is not None:
            return self.players_and_scores[players_tuple].score
        else:
            return 0.0

    def get_players_and_scores(self):
        return self.players_and_scores

    # returns random neighbor of a tuple if it exists, if not it returns original tuple itself
    def get_random_neighbor(self, players_tuple):
        if players_tuple in self.players_and_scores is not None:
            neighbors = self.players_and_scores[players_tuple].neighbours
            if len(neighbors) > 0:
                return random.choice(neighbors)
            else:
                return players_tuple
        else:
            return players_tuple

    def get_all_neighbors(self, players):
        return self.players_and_scores[players].neighbours

    def get_random_players(self):
        return random.choice(list(self.players_and_scores.keys()))

    @staticmethod
    def load_data_from_file(filename):
        file = open(filename, "rb")
        result = pickle.load(file)
        file.close()
        return result
