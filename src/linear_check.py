import time

def linear_search(players_and_scores, max_price):
    best_key = 0
    best_value = 0.0
    start = time.time()
    for k, v in players_and_scores.items():
        if float(v) > best_value and ((int(k[0]) + int(k[3]) + int(k[6]))/3 <= max_price):
            best_key = k
            best_value = float(v)
    end = time.time()
    print("Linear search time = " + (end - start).__str__())

    print(best_key)
    print(best_value)

def linear_search_test(players_and_scores, max_price):
    best_value = 0.0
    start = time.time()
    for k, v in players_and_scores.items():
        if float(v) > best_value and ((int(k[0]) + int(k[3]) + int(k[6]))/3 <= max_price):
            best_value = float(v)
    end = time.time()
    return end-start, best_value