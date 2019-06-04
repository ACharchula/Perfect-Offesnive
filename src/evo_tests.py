from src.SQLiteManager import create_dict_from_file
from src.linear_check import *
from src.evolutionary import Evo, Selection, Data
from prettytable import PrettyTable


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
            price = (int(result[1][0]) + int(result[1][3]) + int(result[1][6])) / 3

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
                                                                                            0.5, 0.2, 100, 99, 200,
                                                                                            13.0)
    x.add_row([10, 200, avg_time, avg_gen, avg_score, high_score, price, 10, accuracy])
    print(x)


def test_evolutionary_algorithm_with_changing_population_size(goal, selection, step, cross_over_prob, mutation_prob,
                                                              pop_size,
                                                              max_price, stagnation,
                                                              expected_result=None, tournSize=None):
    x = PrettyTable()
    x.field_names = ["Population size", "Stagnation", "Avg Time", "Avg Generations", "Avg Score", "Highest Score",
                     "Price", "Repetitions", "Accuracy"]
    n = 20

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
        popSize = pop_size + i * step
    print(x)


def test_evolutionary_algorithm_with_changing_stagnation(goal, selection, step, cross_over_prob, mutation_prob,
                                                         pop_size,
                                                         max_price, stagnation,
                                                         expected_result=None, tournSize=None):
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
        stagnation_ = stagnation + i * step

    print(x)


def test_evolutionary_algorithm_with_decreasing_cross_over_propability(goal, selection, step, cross_over_prob,
                                                                       mutation_prob,
                                                                       pop_size, max_price, stagnation,
                                                                       expected_result=None, tournSize=None):
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
        crspb = crspb - step

    print(x)


def test_evolutionary_algorithm_with_decreasing_mutation_propability(goal, selection, step, cross_over_prob,
                                                                     mutation_prob, pop_size, max_price,
                                                                     stagnation,
                                                                     expected_result=None, tournSize=None):
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
        mtnpb = mtnpb - step

    print(x)


def test_evo():
    run_tests(Data.SHOTONS, Selection.BEST)
    run_tests(Data.SHOTONS, Selection.TOURNAMENT)
    run_tests(Data.GOALS, Selection.BEST)
    run_tests(Data.GOALS, Selection.TOURNAMENT)


def run_tests(data, selection):
    if selection is Selection.TOURNAMENT:
        basic_tourn_size = 10
        for i in range(1, 4):
            test_evolutionary_algorithm_with_changing_population_size(data, selection, 15, 0.85, 0.4, 10, 100, 300, 99,
                                                                      tournSize=basic_tourn_size * i)

        for max_price in range(100, 60, -10):
            if data is Data.SHOTONS:
                linear_result = linear_search_test(create_dict_from_file('players_with_avg_shotons_2.csv'), max_price)
            else:
                linear_result = linear_search_test(create_dict_from_file('players_with_avg_goals_2.csv'), max_price)
            test_evolutionary_algorithm_with_changing_population_size(data, selection, 15, 0.85, 0.4, 10, max_price,
                                                                      300, linear_result[1], tournSize=basic_tourn_size)
            test_evolutionary_algorithm_with_changing_population_size(data, selection, 20, 0.85, 0.4, 100, max_price,
                                                                      300, linear_result[1], tournSize=basic_tourn_size)
            test_evolutionary_algorithm_with_changing_stagnation(data, selection, 15, 0.85, 0.4, 100, max_price, 100,
                                                                 linear_result[1], tournSize=basic_tourn_size)
            test_evolutionary_algorithm_with_changing_stagnation(data, selection, 20, 0.85, 0.4, 100, max_price, 300,
                                                                 linear_result[1], tournSize=basic_tourn_size)
            test_evolutionary_algorithm_with_decreasing_cross_over_propability(data, selection, 0.05, 0.85, 0.4, 100,
                                                                               max_price, 300, linear_result[1],
                                                                               tournSize=basic_tourn_size)
            test_evolutionary_algorithm_with_decreasing_mutation_propability(data, selection, 0.05, 0.85, 0.9, 100,
                                                                             max_price, 300, linear_result[1],
                                                                             tournSize=basic_tourn_size)



    else:
        for max_price in range(100, 60, -10):
            if data is Data.SHOTONS:
                linear_result = linear_search_test(create_dict_from_file('players_with_avg_shotons_2.csv'), max_price)
            else:
                linear_result = linear_search_test(create_dict_from_file('players_with_avg_goals_2.csv'), max_price)
            test_evolutionary_algorithm_with_changing_population_size(data, selection, 15, 0.85,
                                                                      0.4, 10, max_price,
                                                                      300, linear_result[1])
            test_evolutionary_algorithm_with_changing_population_size(data, selection, 20, 0.85, 0.4, 100, max_price,
                                                                      300, linear_result[1])
            test_evolutionary_algorithm_with_changing_stagnation(data, selection, 15, 0.85, 0.4, 100, max_price, 100)
            test_evolutionary_algorithm_with_changing_stagnation(data, selection, 20, 0.85, 0.4, 100, max_price, 300)
            test_evolutionary_algorithm_with_decreasing_cross_over_propability(data, selection, 0.05, 0.85, 0.4, 100,
                                                                               max_price, 300, linear_result[1])
            test_evolutionary_algorithm_with_decreasing_mutation_propability(data, selection, 0.05, 0.85, 0.9, 100,
                                                                             max_price, 300, linear_result[1])
