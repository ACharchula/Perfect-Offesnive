

from src.simanneal_tests import perform_all_simanneal_test

from src.SQLiteManager import create_dict_from_file
from src.structures import AllData
from src.evo_tests import test_evo


players_and_scores = dict()

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
test_evo()
