class Player:

    def __init__(self, overall, shot, finishing):
        self.overall = overall
        self.shot = shot
        self.finishing = finishing

    def __eq__(self, other):
        if other.overall == self.overall and other.shot == self.shot and other.finishing == self.finishing:
            return True
        else:
            return False

    def __str__(self):
        return self.overall + " " + self.shot + " " + self.finishing


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
