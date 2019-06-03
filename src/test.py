import csv

from src.simulated_annealing import *
from src.linear_check import *
from src.structures import AllData
from src.evolutionary import run_evolutionary_algorithm
from prettytable import PrettyTable

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


def simulated_annealing(shotons, value_to_find, max_price, steps, test, Tmax, Tmin):
    if shotons:
        key = random.choice(list(create_dict_from_file('players_with_avg_goals_2.csv').keys()))
        data = AllData.load_data_from_file("przestrzen2.txt")
    else:
        key = random.choice(list(create_dict_from_file('players_with_avg_shotons_2.csv').keys()))
        data = AllData.load_data_from_file("przestrzen.txt")

    # key = ('82', '75', '76', '78', '82', '78', '74', '81', '74')
    if test:
        return perform_simulated_annealing_test(key, data, steps, value_to_find, max_price, Tmax, Tmin)
    else:
        perform_simulated_annealing(key, data, steps, value_to_find, max_price)

    return


def test_simanneal():
    # write_results(False, 7, 100, 30000, 50000.0, 2.5)
    # write_results(False, 7, 100, 30000, 40000.0, 2.5)
    # write_results(False, 7, 100, 30000, 30000.0, 2.5)
    # write_results(False, 7, 100, 30000, -1, -1)
    write_results(True, 13, 100, 10000, -1, -1)


def perform_simanneal(shotons, expected_value, max_cost, steps, Tmax, Tmin):
    if shotons:
        linear_result = linear_search_test(create_dict_from_file('players_with_avg_shotons_2.csv'), max_cost)
    else:
        linear_result = linear_search_test(create_dict_from_file('players_with_avg_goals_2.csv'), max_cost)

    result = 0
    errors = 0
    max_range = 20
    for i in range(0, max_range):
        resultSimanneal = simulated_annealing(shotons, expected_value, max_cost, steps, True, Tmax, Tmin)
        if linear_result[1] != resultSimanneal[1]:
            errors += 1
        else:
            result += resultSimanneal[0]

    return result / (max_range - errors), errors, linear_result[0]


def write_results(shotons, expected_value, max_cost, steps, Tmax, Tmin):
    result = perform_simanneal(shotons, expected_value, max_cost, steps, Tmax, Tmin)
    print('================================================')
    print('PARAMS ' + 'shotons: ' + str(shotons) + ' max_cost: ' + str(expected_value) + ' max_cost: ' + str(
        max_cost) + ' steps: ' + str(steps)
          + ' Tmax: ' + str(Tmax) + ' Tmin: ' + str(Tmin))
    print('simulated annealing speed: ' + str(result[0]))
    print('errors: ' + str(result[1]))
    print('linear speed: ' + str(result[2]))


# test_simanneal()

x = PrettyTable()
x.field_names = ["Population size", "Stagnation", "Time", "Generations", "Best Individual", "Score", "Price"]

for i in range(1, 10):
    pop_size = 6 + i
    stagnation = 200
    start = time.time()
    g, best_ind, score = run_evolutionary_algorithm(0.5, 0.8, pop_size * i, 99, stagnation, 12.0)
    end = time.time()

    print("Generations %s" % g)
    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))
    print("Time is ", end - start)
    x.add_row([pop_size, stagnation, end - start, g, best_ind, score,
               (int(best_ind[0]) + int(best_ind[3]) + int(best_ind[6])) / 3])

print(x)
