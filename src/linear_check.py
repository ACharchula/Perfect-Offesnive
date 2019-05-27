import time

def linear_search(players_and_scores):
    best_key = 0
    best_value = 0.0
    start = time.time()
    for k, v in players_and_scores.items():
        if float(v) > best_value:
            best_key = k
            best_value = float(v)
    end = time.time()
    print("Linear search time = " + (end - start).__str__())

    print(best_key)
    print(best_value)
