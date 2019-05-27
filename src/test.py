import csv

from src.simulated_annealing import *
from src.linear_check import *
from src.structures import AllData

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


def simulated_annealing(shotons):
    key = ('82', '75', '76', '78', '82', '78', '74', '81', '74')

    if shotons:
        data = AllData.load_data_from_file("przestrzen2.txt")
    else:
        data = AllData.load_data_from_file("przestrzen.txt")

    perform_simulated_annealing(key, data, 2500)

simulated_annealing(False)
linear_search(create_dict_from_file('players_with_avg_goals_2.csv'))
simulated_annealing(True)
linear_search(create_dict_from_file('players_with_avg_shotons_2.csv'))