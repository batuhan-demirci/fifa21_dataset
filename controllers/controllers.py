from typing import List
from utils.db_connection_manager import ConnectionManager
from models.models import *


class Controllers:

    def __init__(self):
        """
        This class handles database operations.
        Queries generated from pgAdmin4 web console
        Note: Normally we should parameterize our queries but since this project is not open for any user
        it's okay to use regular Python string formatting.
        """

        # Team insert queries
        self.q_insert_tbl_team_urls = "INSERT INTO public.tbl_team_urls (str_url, dt_crawled) VALUES ('{}', NOW())"
        self.q_insert_tbl_team = "INSERT INTO public.tbl_team(int_team_id, " \
                                 "str_team_name, " \
                                 "str_league, " \
                                 "int_overall, " \
                                 "int_attack, " \
                                 "int_midfield, " \
                                 "int_defence, " \
                                 "int_international_prestige, " \
                                 "int_domestic_prestige, " \
                                 "int_transfer_budget) " \
                                 "VALUES ({}, '{}', '{}', {}, {}, {}, {}, {}, {}, {});"

        self.q_insert_tbl_team_tactics = "INSERT INTO public.tbl_team_tactics(int_team_id, " \
                                         "str_defensive_style, " \
                                         "int_team_width, " \
                                         "int_depth, " \
                                         "str_offensive_style, " \
                                         "int_width, " \
                                         "int_players_in_box, " \
                                         "int_corners, " \
                                         "int_freekicks)" \
                                         "VALUES ({}, '{}', {}, {}, '{}', {}, {}, {}, {});"

        # Team select queries
        self.q_get_team_id_by_url = "SELECT int_team_id " \
                                    "FROM public.tbl_team_urls " \
                                    "WHERE str_url = '{}'"

        self.q_get_tbl_team_urls = "SELECT * " \
                                   "FROM public.tbl_team_urls"

        # Player insert queries
        self.q_insert_tbl_player_urls = "INSERT INTO public.tbl_player_urls (str_url, dt_crawled) VALUES ('{}', NOW())"
        self.q_insert_tbl_player = "INSERT INTO public.tbl_player(int_player_id, " \
                                   "str_player_name, " \
                                   "str_positions, " \
                                   "dt_date_of_birth, " \
                                   "int_height, " \
                                   "int_weight, " \
                                   "int_overall_rating, " \
                                   "int_potential_rating, " \
                                   "str_best_position, " \
                                   "int_best_overall_rating, " \
                                   "int_value, " \
                                   "int_wage, " \
                                   "str_player_image_url, " \
                                   "int_team_id," \
                                   "str_nationality) " \
                                   "VALUES ({}, '{}', '{}', '{}', {}, {}, {}, {}, '{}', {}, {}, {}, '{}', {}, '{}');"
        self.q_insert_tbl_player_attacking = "INSERT INTO public.tbl_player_attacking(int_player_id, " \
                                             "int_crossing, " \
                                             "int_finishing, " \
                                             "int_heading_accuracy, " \
                                             "int_short_passing, " \
                                             "int_volleys) " \
                                             "VALUES ({}, {}, {}, {}, {}, {});"
        self.q_insert_tbl_player_defending = "INSERT INTO public.tbl_player_defending(int_player_id, " \
                                             "int_defensive_awareness, " \
                                             "int_standing_tackle, " \
                                             "int_sliding_tackle) " \
                                             "VALUES ({}, {}, {}, {});"
        self.q_insert_tbl_player_goalkeeping = "INSERT INTO public.tbl_player_goalkeeping(int_player_id, " \
                                               "int_diving, " \
                                               "int_handling, " \
                                               "int_kicking, " \
                                               "int_positioning, " \
                                               "int_reflexes) " \
                                               "VALUES ({}, {}, {}, {}, {}, {});"
        self.q_insert_tbl_player_mentality = "INSERT INTO public.tbl_player_mentality (int_player_id, " \
                                             "int_aggression, " \
                                             "int_interceptions, " \
                                             "int_positioning, " \
                                             "int_vision, " \
                                             "int_penalties, " \
                                             "int_composure) " \
                                             "VALUES ({}, {}, {}, {}, {}, {}, {});"
        self.q_insert_tbl_player_movement = "INSERT INTO public.tbl_player_movement (int_player_id, " \
                                            "int_acceleration, " \
                                            "int_sprint_speed, " \
                                            "int_agility, " \
                                            "int_reactions, " \
                                            "int_balance) " \
                                            "VALUES ({}, {}, {}, {}, {}, {});"
        self.q_insert_tbl_player_power = "INSERT INTO public.tbl_player_power (int_player_id, " \
                                         "int_shot_power, " \
                                         "int_jumping, " \
                                         "int_stamina, " \
                                         "int_strength, " \
                                         "int_long_shots) " \
                                         "VALUES ({}, {}, {}, {}, {}, {});"
        self.q_insert_tbl_player_profile = "INSERT INTO public.tbl_player_profile (int_player_id, " \
                                           "str_preferred_foot, " \
                                           "int_weak_foot, " \
                                           "int_skill_moves, " \
                                           "int_international_reputations, " \
                                           "str_work_rate, " \
                                           "str_body_type) " \
                                           "VALUES ({}, '{}', {}, {}, {}, '{}', '{}');"
        self.q_insert_tbl_player_skill = "INSERT INTO public.tbl_player_skill (int_player_id, " \
                                         "int_dribbling, " \
                                         "int_curve, " \
                                         "int_fk_accuracy, " \
                                         "int_long_passing, " \
                                         "int_ball_control) " \
                                         "VALUES ({}, {}, {}, {}, {}, {});"
        self.q_insert_tbl_player_specialities = "INSERT INTO public.tbl_player_specialities (int_player_id, " \
                                                "str_player_speciality) " \
                                                "VALUES ({}, '{}');"
        self.q_insert_tbl_player_traits = "INSERT INTO public.tbl_player_traits (int_player_id, " \
                                          "str_trait) " \
                                          "VALUES ({}, '{}');"

        # Player select queries
        self.q_get_tbl_player_urls = "SELECT * " \
                                     "FROM public.tbl_player_urls " \
                                     "WHERE int_player_id NOT IN (SELECT int_player_id FROM tbl_player) " \
                                     "LIMIT 500"

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

    def insert_tbl_player(self, tbl_players: List[TblPlayer]):
        with ConnectionManager() as manager:
            for tbl_player in tbl_players:
                q = self.q_insert_tbl_player.format(
                    tbl_player.int_player_id,
                    tbl_player.str_player_name.replace("'", "''"),
                    tbl_player.str_positions.replace("'", "''"),
                    tbl_player.dt_date_of_birth,
                    tbl_player.int_height,
                    tbl_player.int_weight,
                    tbl_player.int_overall_rating,
                    tbl_player.int_potential_rating,
                    tbl_player.str_best_position.replace("'", "''"),
                    tbl_player.int_best_overall_rating,
                    tbl_player.int_value,
                    tbl_player.int_wage,
                    tbl_player.str_player_image_url,
                    tbl_player.int_team_id,
                    tbl_player.str_nationality.replace("'", "''")
                )
                manager.cur.execute(q)
                manager.con.commit()

    def insert_tbl_player_attacking(self, tbl_player_attacking: List[TblPlayerAttacking]):
        with ConnectionManager() as manager:
            for attacking in tbl_player_attacking:
                q = self.q_insert_tbl_player_attacking.format(
                    attacking.int_player_id,
                    attacking.int_crossing,
                    attacking.int_finishing,
                    attacking.int_heading_accuracy,
                    attacking.int_short_passing,
                    attacking.int_volleys
                )
                manager.cur.execute(q)
                manager.con.commit()

    def insert_tbl_player_defending(self, tbl_player_defending: List[TblPlayerDefending]):
        with ConnectionManager() as manager:
            for defending in tbl_player_defending:
                q = self.q_insert_tbl_player_defending.format(
                    defending.int_player_id,
                    defending.int_defensive_awareness,
                    defending.int_standing_tackle,
                    defending.int_sliding_tackle
                )
                manager.cur.execute(q)
                manager.con.commit()

    def insert_tbl_player_goalkeeping(self, tbl_player_goalkeeping: List[TblPlayerGoalkeeping]):
        with ConnectionManager() as manager:
            for goalkeeping in tbl_player_goalkeeping:
                q = self.q_insert_tbl_player_goalkeeping.format(
                    goalkeeping.int_player_id,
                    goalkeeping.int_diving,
                    goalkeeping.int_handling,
                    goalkeeping.int_kicking,
                    goalkeeping.int_positioning,
                    goalkeeping.int_reflexes
                )
                manager.cur.execute(q)
                manager.con.commit()

    def insert_tbl_player_mentality(self, tbl_player_mentality: List[TblPlayerMentality]):
        with ConnectionManager() as manager:
            for mentality in tbl_player_mentality:
                q = self.q_insert_tbl_player_mentality.format(
                    mentality.int_player_id,
                    mentality.int_aggression,
                    mentality.int_interceptions,
                    mentality.int_positioning,
                    mentality.int_vision,
                    mentality.int_penalties,
                    mentality.int_composure
                )
                manager.cur.execute(q)
                manager.con.commit()

    def insert_tbl_player_movement(self, tbl_player_movement: List[TblPlayerMovement]):
        with ConnectionManager() as manager:
            for movement in tbl_player_movement:
                q = self.q_insert_tbl_player_movement.format(
                    movement.int_player_id,
                    movement.int_acceleration,
                    movement.int_sprint_speed,
                    movement.int_agility,
                    movement.int_reactions,
                    movement.int_balance
                )
                manager.cur.execute(q)
                manager.con.commit()

    def insert_tbl_player_power(self, tbl_player_power: List[TblPlayerPower]):
        with ConnectionManager() as manager:
            for power in tbl_player_power:
                q = self.q_insert_tbl_player_power.format(
                    power.int_player_id,
                    power.int_shot_power,
                    power.int_jumping,
                    power.int_stamina,
                    power.int_strength,
                    power.int_long_shots
                )
                manager.cur.execute(q)
                manager.con.commit()

    def insert_tbl_player_profile(self, tbl_player_profile: List[TblPlayerProfile]):
        with ConnectionManager() as manager:
            for profile in tbl_player_profile:
                q = self.q_insert_tbl_player_profile.format(
                    profile.int_player_id,
                    profile.str_preferred_foot.replace("'", "''"),
                    profile.int_weak_foot,
                    profile.int_skill_moves,
                    profile.int_international_reputations,
                    profile.str_work_rate.replace("'", "''"),
                    profile.str_body_type.replace("'", "''")
                )
                manager.cur.execute(q)
                manager.con.commit()

    def insert_tbl_player_skill(self, tbl_player_skill: List[TblPlayerSkill]):
        with ConnectionManager() as manager:
            for skill in tbl_player_skill:
                q = self.q_insert_tbl_player_skill.format(
                    skill.int_player_id,
                    skill.int_dribbling,
                    skill.int_curve,
                    skill.int_fk_accuracy,
                    skill.int_long_passing,
                    skill.int_ball_control
                )
                manager.cur.execute(q)
                manager.con.commit()

    def insert_tbl_player_speciality(self, tbl_player_speciality: List[TblPlayerSpeciality]):
        with ConnectionManager() as manager:
            for speciality_object in tbl_player_speciality:
                for speciality in speciality_object:
                    q = self.q_insert_tbl_player_specialities.format(
                        speciality.int_player_id,
                        speciality.str_player_speciality.replace("'", "''")
                    )
                    manager.cur.execute(q)
                    manager.con.commit()

    def insert_tbl_player_traits(self, tbl_player_traits: List[TblPlayerTrait]):
        with ConnectionManager() as manager:
            for traits_object in tbl_player_traits:
                for traits in traits_object:
                    q = self.q_insert_tbl_player_traits.format(
                        traits.int_player_id,
                        traits.str_trait.replace("'", "''")
                    )
                    manager.cur.execute(q)
                    manager.con.commit()

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
