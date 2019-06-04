import csv

from prettytable import PrettyTable

from src.simanneal_tests import perform_all_simanneal_test
from src.simulated_annealing import *
from src.linear_check import *
from src.structures import AllData
from src.evolutionary import run_evolutionary_algorithm

players_and_scores = dict()


def create_dict_from_file(filename):
    result = dict()

    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            key = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            result[key] = row[9]

    return result


def create_search_space_for_goals():
    players_and_scores = create_dict_from_file('players_with_avg_goals_2.csv')
    data = AllData(players_and_scores)
    data.assign_neighbours()
    data.save_data_to_file("przestrzen.txt")


def create_search_space_for_shotons():
    players_and_scores = create_dict_from_file('players_with_avg_shotons_2.csv')
    data = AllData(players_and_scores)
    data.assign_neighbours()
    data.save_data_to_file("przestrzen2.txt")

perform_all_simanneal_test()

# x = PrettyTable()
# x.field_names = ["Population size", "Stagnation", "Time", "Generations", "Best Individual", "Score", "Price"]
#
# for i in range(1, 10):
#     pop_size = 6 + i
#     stagnation = 200
#     start = time.time()
#     g, best_ind, score = run_evolutionary_algorithm(0.5, 0.8, pop_size * i, 99, stagnation, 12.0)
#     end = time.time()
#
#     print("Generations %s" % g)
#     print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))
#     print("Time is ", end - start)
#     x.add_row([pop_size, stagnation, end - start, g, best_ind, score,
#                (int(best_ind[0]) + int(best_ind[3]) + int(best_ind[6])) / 3])
#
# print(x)
