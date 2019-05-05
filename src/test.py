import csv

from src.simulated_annealing import *

players_and_scores = dict()

with open('players_with_avg_goals.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    count = 0
    for row in csv_reader:
        if count == 0:
            count += 1
            continue
        else:
            key = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            players_and_scores[key] = row[9]
            count += 1

print(f'Processed {count} lines.')

data = AllData(players_and_scores)
