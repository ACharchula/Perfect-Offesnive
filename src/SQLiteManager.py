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


def get_unique_players_and_avg_score(conn, shotons):
    matches_dictionary = dict()

    matches = select_all_matches_with_player_stats_and_goals(conn, shotons)

    for match in matches:
        key = (match[0], match[1], match[2], match[3], match[4], match[5], match[6], match[7], match[8])

        if key in matches_dictionary:
            matches_dictionary[key].append(match[9])
        else:
            matches_dictionary[key] = [match[9]]

    player_dictionary = dict()

    for k, v in matches_dictionary.items():
        player_dictionary[k] = (sum(v) / len(v))

    return player_dictionary


def select_all_matches_with_player_stats_and_goals(conn, shotons):
    cur = conn.cursor()

    if shotons:
        cur.execute(
            "SELECT home_player_9, home_player_10, home_player_11, shoton FROM Match WHERE home_player_9 is not NULL AND home_player_10 is not NULL AND home_player_11 is not NULL AND shoton is not NULL")
        home_players = cur.fetchall()
        cur.execute(
            "SELECT away_player_9, away_player_10, away_player_11, shoton FROM Match WHERE away_player_9 is not NULL AND away_player_10 is not NULL AND away_player_11 is not NULL AND shoton is not NULL")
        away_players = cur.fetchall()

    else:
        cur.execute(
            "SELECT home_player_9, home_player_10, home_player_11, goal FROM Match WHERE home_player_9 is not NULL AND home_player_10 is not NULL AND home_player_11 is not NULL AND goal is not NULL")
        home_players = cur.fetchall()
        cur.execute(
            "SELECT away_player_9, away_player_10, away_player_11, goal FROM Match WHERE away_player_9 is not NULL AND away_player_10 is not NULL AND away_player_11 is not NULL AND goal is not NULL")
        away_players = cur.fetchall()

    p1 = change_id_to_player_stats_and_count_goals(home_players, conn)
    p2 = change_id_to_player_stats_and_count_goals(away_players, conn)

    p1.extend(p2)

    return p1


def change_id_to_player_stats_and_count_goals(rows, conn):
    players = select_all_players_with_newest_stats(conn)
    matches = list()

    for row in rows:
        goals = 0

        goals += row[3].count('<player1>' + str(row[0]) + '</player1>')
        goals += row[3].count('<player1>' + str(row[1]) + '</player1>')
        goals += row[3].count('<player1>' + str(row[2]) + '</player1>')

        p1 = players[row[0]]
        p2 = players[row[1]]
        p3 = players[row[2]]
        l = list()
        l.append(p1[0])
        l.append(p1[1])
        l.append(p1[2])

        l.append(p2[0])
        l.append(p2[1])
        l.append(p2[2])

        l.append(p3[0])
        l.append(p3[1])
        l.append(p3[2])

        l.append(goals)
        result = tuple(l)
        matches.append(result)

    return matches


def select_all_players_with_newest_stats(conn):
    cur = conn.cursor()
    cur.execute("SELECT p.player_api_id, p.overall_rating, p.shot_power, p.finishing"
                " FROM Player_Attributes AS p "
                "JOIN (SELECT x.player_api_id, MAX(x.date) AS max_date "
                "FROM Player_Attributes AS x "
                "GROUP BY x.player_api_id) y "
                "ON y.player_api_id = p.player_api_id AND y.max_date = p.date "
                "WHERE p.overall_rating is not NULL AND p.shot_power is not NULL AND p.finishing is not NULL ")

    result = cur.fetchall()
    all_player_dict = dict()

    for player in result:
        all_player_dict[player[0]] = (player[1], player[2], player[3])

    return all_player_dict


def select_all_players_with_given_parameters(conn, overall, power, finish):
    cur = conn.cursor()
    cur.execute("SELECT p.player_api_id, p.overall_rating, p.shot_power, p.finishing"
                " FROM Player_Attributes AS p "
                "JOIN (SELECT x.player_api_id, MAX(x.date) AS max_date "
                "FROM Player_Attributes AS x GROUP BY x.player_api_id) y "
                "ON y.player_api_id = p.player_api_id AND y.max_date = p.date "
                "WHERE p.overall_rating=? AND p.shot_power=? AND p.finishing=? "
                "GROUP BY p.player_api_id, p.date", (overall, power, finish,))

    rows = cur.fetchall()

    for row in rows:
        print(row)


def save_to_csv(filename, data):
    with open(filename, mode='w') as players_file:
        player_writer = csv.writer(players_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for key, value in data.items():
            player_writer.writerow([key[0], key[1], key[2], key[3], key[4], key[5], key[6], key[7], key[8], value])


def add_goals_to_shotons(goals, shotons):
    result = dict()

    for key, value in shotons.items():
        result[key] = value + goals[key]

    return result


def create_data_csv_files():
    database = "./database.sqlite"
    conn = create_connection(database)

    players_goals = get_unique_players_and_avg_score(conn, False)
    players_shotons = get_unique_players_and_avg_score(conn, True)

    save_to_csv('players_with_avg_goals_2.csv', players_goals)

    players_shotons_final = add_goals_to_shotons(players_goals, players_shotons)
    save_to_csv('players_with_avg_shotons_2.csv', players_shotons_final)


create_data_csv_files()