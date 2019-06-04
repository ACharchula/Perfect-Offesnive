import csv

from src.simulated_annealing import *
from src.linear_check import *
from src.structures import AllData
from src.evolutionary import Evo, Selection, Data
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




def run_n_times_and_gather_info(n, expected_result, func_to_run, *args):
    results = []
    times = []
    highest_score = 0
    good = 0
    price = 0
    for i in range(0, n):
        start = time.time()
        result = func_to_run(*args)
        end = time.time()

        if result[2][0] > highest_score:
            highest_score = result[2][0]
            price = (int(result[1][0]) + int(result[1][3] )+ int(result[1][6])) / 3

        if result[2][0] == expected_result:
            good = good + 1

        results.append(result)
        times.append(end - start)

    sum = 0
    generations = 0
    total_time = 0
    for time_ in times:
        total_time += time_
    for elem in results:
        sum += elem[2][0]
        generations += elem[0]

    return generations / len(results), sum / len(results), total_time / len(results), highest_score, good / n, price


def test_one_set_of_parameters():
    x = PrettyTable()
    x.field_names = ["Population size", "Stagnation", "Avg Time", "Avg Generations", "Avg Score", "Highest Score",
                     "Price", "Repetitions", "Accuracy"]

    evo = Evo(Data.SHOTONS, Selection.BEST)
    avg_gen, avg_score, avg_time, high_score, accuracy, price = run_n_times_and_gather_info(10, 13,
                                                                                     evo.run_evolutionary_algorithm,
                                                                                     0.5, 0.2, 100, 99, 200, 13.0)
    x.add_row([10, 200, avg_time, avg_gen, avg_score, high_score, price, 10, accuracy])
    print(x)


def test_evolutionary_algorithm_with_changing_population_size(goal, selection, cross_over_prob, mutation_prob, pop_size,
                                                              max_price, stagnation,
                                                              expected_result, tournSize=None):
    print("Pop size= %s; cross_over_probabilty= %s; mutation_propability=%s" %(pop_size,cross_over_prob,mutation_prob))
    x = PrettyTable()
    x.field_names = ["Population size", "Stagnation", "Avg Time", "Avg Generations", "Avg Score", "Highest Score",
                     "Price", "Repetitions", "Accuracy"]
    n = 10

    evo = Evo(goal, selection, tournSize=tournSize)
    popSize = pop_size
    for i in range(1, 10):
        avg_gen, avg_score, avg_time, high_score, accuracy, price = run_n_times_and_gather_info(n, expected_result,
                                                                                                evo.run_evolutionary_algorithm,
                                                                                                cross_over_prob,
                                                                                                mutation_prob,
                                                                                                popSize, max_price,
                                                                                                stagnation,
                                                                                                expected_result)

        x.add_row([popSize, stagnation, avg_time, avg_gen, avg_score, high_score, price, n, accuracy])
        popSize = pop_size + i * 10
    print(x)

def test_evolutionary_algorithm_with_changing_stagnation(goal, selection, cross_over_prob, mutation_prob, pop_size,
                                                         max_price, stagnation,
                                                         expected_result, tournSize=None):
    x = PrettyTable()
    x.field_names = ["Population size", "Stagnation", "Avg Time", "Avg Generations", "Avg Score", "Highest Score",
                     "Price", "Repetitions", "Accuracy"]
    n = 20

    evo = Evo(goal, selection, tournSize=tournSize)
    stagnation_ = stagnation
    for i in range(1, 10):
        avg_gen, avg_score, avg_time, high_score, accuracy, price = run_n_times_and_gather_info(n, expected_result,
                                                                                         evo.run_evolutionary_algorithm,
                                                                                         cross_over_prob,
                                                                                         mutation_prob,
                                                                                         pop_size, max_price,
                                                                                         stagnation_,
                                                                                         expected_result)

        x.add_row([pop_size, stagnation_, avg_time, avg_gen, avg_score, high_score, price, n, accuracy])
        stagnation_ = stagnation + i * 20

    print(x)


def test_evolutionary_algorithm_with_decreasing_cross_over_propability(goal, selection, cross_over_prob, mutation_prob,
                                                                       pop_size, max_price, stagnation,
                                                                       expected_result, tournSize=None):
    x = PrettyTable()
    x.field_names = ["Population size", "Stagnation", "Avg Time", "Avg Generations", "Avg Score", "Highest Score",
                     "Price", "Repetitions", "Accuracy", "CRSPB"]
    n = 20

    evo = Evo(goal, selection, tournSize=tournSize)
    crspb = cross_over_prob
    for i in range(1, 10):
        avg_gen, avg_score, avg_time, high_score, accuracy, price = run_n_times_and_gather_info(n, expected_result,
                                                                                         evo.run_evolutionary_algorithm,
                                                                                         crspb,
                                                                                         mutation_prob,
                                                                                         pop_size, max_price,
                                                                                         stagnation,
                                                                                         expected_result)

        x.add_row([pop_size, stagnation, avg_time, avg_gen, avg_score, high_score, price, n, accuracy, crspb])
        crspb = crspb - 0.75

    print(x)


def test_evolutionary_algorithm_with_decreasing_mutation_propability(goal, selection, cross_over_prob,
                                                                       mutation_prob, pop_size, max_price,
                                                                       stagnation,
                                                                       expected_result, tournSize=None):
    x = PrettyTable()
    x.field_names = ["Population size", "Stagnation", "Avg Time", "Avg Generations", "Avg Score", "Highest Score",
                     "Price", "Repetitions", "Accuracy", "MTNPB"]
    n = 20

    evo = Evo(goal, selection, tournSize=tournSize)
    mtnpb = mutation_prob
    for i in range(1, 10):
        avg_gen, avg_score, avg_time, high_score, accuracy, price = run_n_times_and_gather_info(n, expected_result,
                                                                                         evo.run_evolutionary_algorithm,
                                                                                         cross_over_prob,
                                                                                         mtnpb,
                                                                                         pop_size, max_price,
                                                                                         stagnation,
                                                                                         expected_result)

        x.add_row([pop_size, stagnation, avg_time, avg_gen, avg_score, high_score, price, n, accuracy, mtnpb])
        mtnpb = mtnpb - 0.75

    print(x)


test_evolutionary_algorithm_with_changing_population_size(Data.SHOTONS, Selection.BEST, 0.85, 0.4, 100, 99, 400,
                                                                   13.0)
