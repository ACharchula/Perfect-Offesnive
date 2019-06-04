from prettytable import PrettyTable
from src.simulated_annealing import *
from src.linear_check import *
from src.structures import AllData
import csv


def create_dict_from_file(filename):
    result = dict()

    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            key = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            result[key] = row[9]

    return result

def test_simanneal_shotons(max_price):
    linear_result = linear_search_test(create_dict_from_file('players_with_avg_shotons_2.csv'), max_price)
    all_simanneal_tests_shotons(max_price, linear_result)

def test_simanneal_goals(max_price):
    linear_result = linear_search_test(create_dict_from_file('players_with_avg_goals_2.csv'), max_price)
    all_simanneal_tests_goals(max_price, linear_result)

def all_simanneal_tests_shotons(max_price, linear_result):

    x = PrettyTable()
    x.field_names = ["Steps", "Tmax", "Tmin", "Stagnation", "Avg time", "Wrong results", "Iterations"]

    result = perform_simanneal(True, linear_result[1], max_price, 30000, -1, -1, -1, linear_result, 10)
    x.add_row([result[0], result[1], result[2], result[3], result[4], result[5], result[6]])
    result = perform_simanneal(True, -1, max_price, 1000, -1, -1, -1, linear_result, 10)
    x.add_row([result[0], result[1], result[2], result[3], result[4], result[5], result[6]])

    test_stagnation(True, linear_result, x, max_price)
    test_tmax(True, linear_result, x, max_price)
    test_tmin(True, linear_result, x, max_price)

    print()
    header = "SHOTONS Max price: " + str(max_price) + " Linear time: " + str(linear_result[0]) + " Result: " + str(linear_result[1])
    print(header)
    print(x)
    print()
    with open('simmaneal_results', 'a+') as w:
        w.write(header)
        w.write(str(x))

def all_simanneal_tests_goals(max_price, linear_result):

    x = PrettyTable()
    x.field_names = ["Steps", "Tmax", "Tmin", "Stagnation", "Avg time", "Wrong results", "Iterations"]

    result = perform_simanneal(False, linear_result[1], max_price, 30000, -1, -1, -1, linear_result, 10)
    x.add_row([result[0], result[1], result[2], result[3], result[4], result[5], result[6]])
    result = perform_simanneal(False, -1, max_price, 1000, -1, -1, -1, linear_result, 10)
    x.add_row([result[0], result[1], result[2], result[3], result[4], result[5], result[6]])

    test_stagnation(False, linear_result, x, max_price)

    test_tmax(False, linear_result, x, max_price)
    test_tmin(False, linear_result, x, max_price)

    print()
    header = "GOALS Max price: " + str(max_price) + " Linear time: " + str(linear_result[0]) + " Result: " + str(linear_result[1])
    print(header)
    print(x)
    print()
    with open('simmaneal_results', 'a+') as w:
        w.write(header)
        w.write(str(x))


def test_stagnation(shoton, linear_result, table, max_price):
    result = perform_simanneal(shoton, -1, max_price, 30000, -1, -1, 500, linear_result, 5)
    table.add_row([result[0], result[1], result[2], result[3], result[4], result[5], result[6]])
    result = perform_simanneal(shoton, -1, max_price, 30000, -1, -1, 1000, linear_result, 5)
    table.add_row([result[0], result[1], result[2], result[3], result[4], result[5], result[6]])
    result = perform_simanneal(shoton, -1, max_price, 30000, -1, -1, 1500, linear_result, 5)
    table.add_row([result[0], result[1], result[2], result[3], result[4], result[5], result[6]])
    result = perform_simanneal(shoton, -1, max_price, 30000, -1, -1, 2000, linear_result, 5)
    table.add_row([result[0], result[1], result[2], result[3], result[4], result[5], result[6]])
    result = perform_simanneal(shoton, -1, max_price, 30000, -1, -1, 2500, linear_result, 5)
    table.add_row([result[0], result[1], result[2], result[3], result[4], result[5], result[6]])
    result = perform_simanneal(shoton, -1, max_price, 30000, -1, -1, 3000, linear_result, 5)
    table.add_row([result[0], result[1], result[2], result[3], result[4], result[5], result[6]])
    result = perform_simanneal(shoton, -1, max_price, 30000, -1, -1, 3500, linear_result, 5)
    table.add_row([result[0], result[1], result[2], result[3], result[4], result[5], result[6]])

def test_tmax(shoton, linear_result, table, max_price):
    result = perform_simanneal(shoton, -1, max_price, 10000, 250, 0.3, -1, linear_result, 5)
    table.add_row([result[0], result[1], result[2], result[3], result[4], result[5], result[6]])
    result = perform_simanneal(shoton, -1, max_price, 10000, 200, 0.3, -1, linear_result, 5)
    table.add_row([result[0], result[1], result[2], result[3], result[4], result[5], result[6]])
    result = perform_simanneal(shoton, -1, max_price, 10000, 150, 0.3, -1, linear_result, 5)
    table.add_row([result[0], result[1], result[2], result[3], result[4], result[5], result[6]])
    result = perform_simanneal(shoton, -1, max_price, 10000, 100, 0.3, -1, linear_result, 5)
    table.add_row([result[0], result[1], result[2], result[3], result[4], result[5], result[6]])
    result = perform_simanneal(shoton, -1, max_price, 10000, 50, 0.3, -1, linear_result, 5)
    table.add_row([result[0], result[1], result[2], result[3], result[4], result[5], result[6]])

def test_tmin(shoton, linear_result, table, max_price):
    result = perform_simanneal(shoton, -1, max_price, 10000, -1, 4, -1, linear_result, 5)
    table.add_row([result[0], result[1], result[2], result[3], result[4], result[5], result[6]])
    result = perform_simanneal(shoton, -1, max_price, 10000, -1, 3, -1, linear_result, 5)
    table.add_row([result[0], result[1], result[2], result[3], result[4], result[5], result[6]])
    result = perform_simanneal(shoton, -1, max_price, 10000, -1, 2, -1, linear_result, 5)
    table.add_row([result[0], result[1], result[2], result[3], result[4], result[5], result[6]])
    result = perform_simanneal(shoton, -1, max_price, 10000, -1, 1, -1, linear_result, 5)
    table.add_row([result[0], result[1], result[2], result[3], result[4], result[5], result[6]])
    result = perform_simanneal(shoton, -1, max_price, 10000, -1, 0.5, -1, linear_result, 5)
    table.add_row([result[0], result[1], result[2], result[3], result[4], result[5], result[6]])



def perform_simanneal(shotons, expected_value, max_cost, steps, Tmax, Tmin, stagnation, linear_result, max_range):
    result = 0
    errors = 0
    all_steps = 0
    temp_max = 0
    temp_min = 0
    wrong_results = list()
    for i in range(0, max_range):
        resultSimanneal = simulated_annealing(shotons, expected_value, max_cost, steps, True, Tmax, Tmin, stagnation)
        temp_max += resultSimanneal[3]
        temp_min += resultSimanneal[4]
        all_steps += resultSimanneal[5]
        if linear_result[1] != resultSimanneal[1]:
            errors += 1
            wrong_results.append(resultSimanneal[1])
        else:
            result += resultSimanneal[0]

    if max_range - errors == 0:
        result = 0
    else:
        result = result / (max_range - errors)

    return all_steps/max_range, temp_max/max_range, temp_min/max_range, stagnation, result, wrong_results, max_range

def simulated_annealing(shotons, value_to_find, max_price, steps, test, Tmax, Tmin, stagnation):
    if shotons:
        key = random.choice(list(create_dict_from_file('players_with_avg_goals_2.csv').keys()))
        data = AllData.load_data_from_file("przestrzen2.txt")
    else:
        key = random.choice(list(create_dict_from_file('players_with_avg_shotons_2.csv').keys()))
        data = AllData.load_data_from_file("przestrzen.txt")

    # key = ('82', '75', '76', '78', '82', '78', '74', '81', '74')
    if test:
        return perform_simulated_annealing_test(key, data, steps, value_to_find, max_price, Tmax, Tmin, stagnation)
    else:
        perform_simulated_annealing(key, data, steps, value_to_find, max_price, stagnation)

    return

def perform_all_simanneal_test():
    test_simanneal_goals(100)
    test_simanneal_goals(90)
    test_simanneal_goals(80)
    test_simanneal_goals(70)

    test_simanneal_shotons(100)
    test_simanneal_shotons(90)
    test_simanneal_shotons(80)
    test_simanneal_shotons(70)