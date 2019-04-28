import sqlite3
from sqlite3 import Error
import csv


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def select_all_uniqe_matches(conn):

    cur = conn.cursor()
    cur.execute("SELECT DISTINCT home_player_9, home_player_10, home_player_11 FROM Match")

    rows = cur.fetchall()

    i = 0
    for row in rows:
        i += 1
        print(row)

    print(i)

def get_unique_players_and_avg_score(conn):
    matches_dictionary = dict()

    matches = select_all_matches_with_player_stats_and_goals(conn)

    for match in matches:
        key = (match[0], match[1], match[2], match[3], match[4], match[5], match[6], match[7], match[8])

        if key in matches_dictionary:
            matches_dictionary[key].append(match[9])
        else:
            matches_dictionary[key] = [match[9]]

    player_dictionary = dict()

    for k, v in matches_dictionary.items():
        player_dictionary[k] = ( sum(v) / len(v) )

    return player_dictionary


def select_all_matches_with_player_stats_and_goals(conn):

    cur = conn.cursor()
    ##cur.execute("SELECT home_player_9, home_player_10, home_player_11, goal FROM Match")
    cur.execute("SELECT home_player_9, home_player_10, home_player_11, shoton FROM Match")
    home_players = cur.fetchall()

    ##cur.execute("SELECT away_player_9, away_player_10, away_player_11, goal FROM Match")
    cur.execute("SELECT away_player_9, away_player_10, away_player_11, shoton FROM Match")
    away_players = cur.fetchall()

    p1 = change_id_to_player_stats_and_count_goals(home_players)
    p2 = change_id_to_player_stats_and_count_goals(away_players)

    p1.extend(p2)

    return p1


def change_id_to_player_stats_and_count_goals(rows):

    players = select_all_players_with_newest_stats(conn)
    matches = list()

    for row in rows:
        if row[0] is None or row[1] is None or row[2] is None:
            continue

        goals = 0

        if row[3] is not None:
            goals += row[3].count(str(row[0]))
            goals += row[3].count(str(row[1]))
            goals += row[3].count(str(row[2]))

        p1 = [item for item in players if item[0] == row[0]]
        p2 = [item for item in players if item[0] == row[1]]
        p3 = [item for item in players if item[0] == row[2]]
        l = list()
        l.append(p1[0][2])
        l.append(p1[0][3])
        l.append(p1[0][4])

        l.append(p2[0][2])
        l.append(p2[0][3])
        l.append(p2[0][4])

        l.append(p3[0][2])
        l.append(p3[0][3])
        l.append(p3[0][4])

        l.append(goals)
        result = tuple(l)
        matches.append(result)

    print(len(matches))

    return matches

def select_all_players_with_newest_stats(conn):

    cur = conn.cursor()
    cur.execute("SELECT p.player_api_id, p.date, p.overall_rating, p.shot_power, p.finishing"
                " FROM Player_Attributes AS p "
                "JOIN (SELECT x.player_api_id, MAX(x.date) AS max_date "
                "FROM Player_Attributes AS x "
                "GROUP BY x.player_api_id) y "
                "ON y.player_api_id = p.player_api_id AND y.max_date = p.date "
                "WHERE p.overall_rating is not NULL AND p.shot_power is not NULL AND p.finishing is not NULL "
                "GROUP BY p.player_api_id, p.date")

    return cur.fetchall()

def select_all_players_with_given_parameters(conn, overall, power, finish):

    cur = conn.cursor()
    cur.execute("SELECT p.player_api_id, p.date, p.overall_rating, p.shot_power, p.finishing"
                " FROM Player_Attributes AS p "
                "JOIN (SELECT x.player_api_id, MAX(x.date) AS max_date "
                "FROM Player_Attributes AS x GROUP BY x.player_api_id) y "
                "ON y.player_api_id = p.player_api_id AND y.max_date = p.date "
                "WHERE p.overall_rating=? AND p.shot_power=? AND p.finishing=? "
                "GROUP BY p.player_api_id, p.date", (overall, power, finish,))

    rows = cur.fetchall()

    for row in rows:
        print(row)


database = "./database.sqlite"

# create a database connection
conn = create_connection(database)
# select_all_uniqe_matches(conn)
# players = select_all_players_with_newest_stats(conn)
# print(players)

players = get_unique_players_and_avg_score(conn)
len(players)

with open('players_with_avg_shotons.csv', mode='w') as players_file:
    player_writer = csv.writer(players_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    player_writer.writerow(['p1_overall_rating', 'p1_shot_power', 'p1_finishing',
                            'p2_overall_rating', 'p2_shot_power', 'p2_finishing',
                            'p3_overall_rating', 'p3_shot_power', 'p3_finishing',
                            'avg_shotons'])

    for key, value in players.items():
        player_writer.writerow([key[0], key[1], key[2], key[3], key[4], key[5], key[6], key[7], key[8], value])

# for player in players:
#     print()
#     select_all_players_with_given_parameters(conn, player[2], player[3], player[4])
