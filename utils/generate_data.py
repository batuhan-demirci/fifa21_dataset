import pandas as pd
from utils.db_connection_manager import ConnectionManager

""" This module generates csv files for each table """

queries = [('./data/tbl_player_urls.csv', 'SELECT * FROM tbl_player_urls;'),
           ('./data/tbl_player.csv', 'SELECT * FROM tbl_player;'),
           ('./data/tbl_player_attacking.csv', 'SELECT * FROM tbl_player_attacking;'),
           ('./data/tbl_player_defending.csv', 'SELECT * FROM tbl_player_defending;'),
           ('./data/tbl_player_goalkeeping.csv', 'SELECT * FROM tbl_player_goalkeeping;'),
           ('./data/tbl_player_mentality.csv', 'SELECT * FROM tbl_player_mentality;'),
           ('./data/tbl_player_movement.csv', 'SELECT * FROM tbl_player_movement;'),
           ('./data/tbl_player_power.csv', 'SELECT * FROM tbl_player_power;'),
           ('./data/tbl_player_profile.csv', 'SELECT * FROM tbl_player_profile;'),
           ('./data/tbl_player_skill.csv', 'SELECT * FROM tbl_player_skill;'),
           ('./data/tbl_player_specialities.csv', 'SELECT * FROM tbl_player_specialities;'),
           ('./data/tbl_player_traits.csv', 'SELECT * FROM tbl_player_traits;'),
           ('./data/tbl_team_urls.csv', 'SELECT * FROM tbl_team_urls;'),
           ('./data/tbl_team.csv', 'SELECT * FROM tbl_team;'),
           ('./data/tbl_team_tactics.csv', 'SELECT * FROM tbl_team_tactics;')]


def generate():
    with ConnectionManager() as manager:
        for query in queries:
            manager.cur.execute(query[1])
            result = manager.cur.fetchall()

            # Column names
            col_names = []

            for name in manager.cur.description:
                col_names.append(name[0])

            df = pd.DataFrame(result, columns=col_names)
            df.to_csv(query[0], index=False)
