from utils.db_connection_manager import ConnectionManager
from models.models import TblTeamUrl, TblPlayerUrl


class Controllers:

    q_insert_tbl_team_urls = "INSERT INTO tbl_team_urls (str_url, dt_crawled) VALUES ('{}', NOW())"

    q_insert_tbl_player_urls = "INSERT INTO tbl_player_urls (str_url, dt_crawled) VALUES ('{}', NOW())"

    q_insert_tbl_team = "INSERT INTO public.tbl_team(int_team_id, " \
                        "str_team_name, str_league, int_overall, int_attack, int_midfield, " \
                        "int_defence, int_international_prestige, int_domestic_prestige, int_transfer_budget) " \
                        "VALUES ({}, '{}', '{}', {}, {}, {}, {}, {}, {}, {});"

    q_insert_tbl_team_tactics = "INSERT INTO public.tbl_team_tactics(int_team_id, " \
                                "str_defensive_style, int_team_width, int_depth, " \
                                "str_offensive_style, int_width, int_players_in_box, " \
                                "int_corners, int_freekicks)" \
                                "VALUES ({}, '{}', {}, {}, '{}', {}, {}, {}, {});"

    q_get_team_id_by_url = "SELECT int_team_id " \
                           "FROM tbl_team_urls " \
                           "WHERE str_url = '{}'"

    q_get_tbl_team_urls = "SELECT * " \
                          "FROM tbl_team_urls"

    q_get_tbl_player_urls = "SELECT * " \
                            "FROM tbl_player_urls " \
                            "WHERE int_player_id NOT IN (SELECT int_player_id FROM tbl_player) " \
                            "LIMIT 500"

    def __init__(self):
        pass

    def insert_tbl_team_urls(self, tbl_team_urls):
        with ConnectionManager() as manager:
            for team_url in tbl_team_urls:
                manager.cur.execute(self.q_insert_tbl_team_urls.format(team_url))
                manager.con.commit()

    def insert_tbl_team(self, tbl_teams):
        with ConnectionManager() as manager:
            for tbl_team in tbl_teams:
                q = self.q_insert_tbl_team.format(tbl_team.int_team_id,
                                                  tbl_team.str_team_name.replace("'", "''"),  # Escape single quotes
                                                  tbl_team.str_league.replace("'", "''"),
                                                  tbl_team.int_overall,
                                                  tbl_team.int_attack,
                                                  tbl_team.int_midfield,
                                                  tbl_team.int_defence,
                                                  tbl_team.int_international_prestige,
                                                  tbl_team.int_domestic_prestige,
                                                  tbl_team.int_transfer_budget)
                manager.cur.execute(q)
                manager.con.commit()

    def insert_tbl_team_tactic(self, tbl_team_tactics):
        with ConnectionManager() as manager:
            for tbl_team_tactic in tbl_team_tactics:

                # TODO look for better escaping
                q = self.q_insert_tbl_team_tactics.format(tbl_team_tactic.int_team_id,
                                                          tbl_team_tactic.str_defensive_style.replace("'", "''"),
                                                          tbl_team_tactic.int_team_width,
                                                          tbl_team_tactic.int_depth,
                                                          tbl_team_tactic.str_offensive_style.replace("'", "''"),
                                                          tbl_team_tactic.int_width,
                                                          tbl_team_tactic.int_players_in_box,
                                                          tbl_team_tactic.int_corners,
                                                          tbl_team_tactic.int_freekicks)
                manager.cur.execute(q)
                manager.con.commit()

    def insert_tbl_player_urls(self, tbl_player_urls):
        with ConnectionManager() as manager:
            for player_url in tbl_player_urls:
                manager.cur.execute(self.q_insert_tbl_player_urls.format(player_url))
                manager.con.commit()

    def insert_tbl_player(self, tbl_players):
        pass

    def insert_tbl_player_attacking(self, tbl_player_attacking):
        pass

    def insert_tbl_player_defending(self, tbl_player_defending):
        pass

    def insert_tbl_player_goalkeeping(self, tbl_player_goalkeeping):
        pass

    def insert_tbl_player_mentality(self, tbl_player_mentality):
        pass

    def insert_tbl_player_movement(self, tbl_player_movement):
        pass

    def insert_tbl_player_power(self, tbl_player_power):
        pass

    def insert_tbl_player_profile(self, tbl_player_profile):
        pass

    def insert_tbl_player_skill(self, tbl_player_skill):
        pass

    def insert_tbl_player_speciality(self, tbl_player_speciality):
        pass

    def insert_tbl_player_traits(self, tbl_player_traits):
        pass

    def get_team_id_by_url(self, tbl_team_url):
        with ConnectionManager() as manager:
            manager.cur.execute(self.q_get_team_id_by_url.format(tbl_team_url))
            result = manager.cur.fetchone()

            if result is not None:
                return result[0]
            else:
                return None

    def get_tbl_team_urls(self):
        """ Returns every tbl_team_urls """
        tbl_team_urls = []

        with ConnectionManager() as manager:
            manager.cur.execute(self.q_get_tbl_team_urls)
            rows = manager.cur.fetchall()

            for row in rows:
                tbl_team_url = TblTeamUrl()
                tbl_team_url.int_team_id = row[0]
                tbl_team_url.str_url = row[1]
                tbl_team_url.dt_crawled = row[2]
                tbl_team_urls.append(tbl_team_url)
        return tbl_team_urls

    def get_tbl_player_urls(self):
        """ Returns 500 not crawled tbl_player_urls """
        tbl_player_urls = []

        with ConnectionManager() as manager:
            manager.cur.execute(self.q_get_tbl_player_urls)
            rows = manager.cur.fetchall()

            for row in rows:
                tbl_player_url = TblPlayerUrl()
                tbl_player_url.int_player_id = row[0]
                tbl_player_url.str_url = row[1]
                tbl_player_url.dt_crawled = row[2]
                tbl_player_urls.append(tbl_player_url)
        return tbl_player_urls
