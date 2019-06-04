from src.evo_tests import test_evo
from src.linear_check import linear_search_test
from src.simanneal_tests import simulated_annealing, perform_all_simanneal_test, create_dict_from_file

print("1 - Simulated Annealing Search")
print("2 - Evolution Algorithm Search")
print("3 - Simulated Annealing Tests")
print("4 - Evolution Algorithm Tests")

inp = input("Insert number: ")
user_input = int(inp)

if 1 > user_input > 4:
    print("Wrong number")
elif user_input == 1:
    print("1 - Goals search")
    print("2 - Shotons search")
    shotons = input("Write 1 or 2")
    value_to_find = input("Write value to find or -1")
    max_price = input("Write max price")
    steps = input("Write amount of steps")
    tmax = input("Write maximal temperature or -1")
    tmin = input("Write mainimal temperature or -1")
    stagnation = input("Write stagnation or -1")

    if shotons == "1":
        linear_result = linear_search_test(create_dict_from_file('players_with_avg_goals_2.csv'), float(max_price))
        shotons = False
    elif shotons == "2":
        linear_result = linear_search_test(create_dict_from_file('players_with_avg_shotons_2.csv'), float(max_price))
        shotons = True

    simulated_annealing(shotons, float(value_to_find), float(max_price), float(steps), False, float(tmax), float(tmin), int(stagnation))
    print("Correct answer: " + str(linear_result[1]))
elif user_input == 2:
    print("TODO")
elif user_input == 3:
    print("Tests executed, result will be also in file simanneal_results.txt")
    perform_all_simanneal_test()
elif user_input == 4:
    print("Tests executed, result will be also in file evo_tests.txt")
    test_evo()