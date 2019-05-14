def correct_result(players_and_scores):
    best_key = 0
    best_value = 0.0
    for k, v in players_and_scores.items():
        if float(v) > best_value:
            best_key = k
            best_value = float(v)

    print(best_key)
    print(best_value)
