import csv

from src.simulated_annealing import *
from src.linear_check import *
from src.structures import AllData

players_and_scores = dict()

with open('players_with_avg_goals_2.csv') as csv_file:
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

key = ('82','75','76','78','82','78','74','81','74')
# data = AllData(players_and_scores)
# data.assign_neighbours()
# data.save_data_to_file("przestrzen.txt")
data = AllData.load_data_from_file("przestrzen.txt")

perform_simulated_annealing(key, data, 700)
correct_result(players_and_scores)

# dodac takie cos co zauwazy ze od 100 krokow wybieramy to samo