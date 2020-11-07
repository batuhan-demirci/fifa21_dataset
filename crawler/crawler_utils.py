from models.models import *
import re

class CrawlerUtils:

    def __init__(self):

        # tbl_team
        self.team_str_team_name_selector = "#list > div:nth-child(4) > div > div > div.column.col-12 > div > " \
                                           "div:nth-child(1) > div > div > h1"
        self.team_str_league_selector = "#list > div:nth-child(4) > div > div > div.column.col-12 > div > " \
                                        "div:nth-child(1) > div > div > div > a:nth-child(2)"
        self.team_int_overall_selector = "#list > div:nth-child(4) > div > div > div.column.col-12 > div > " \
                                         "div:nth-child(1) > div > section > div > div:nth-child(1) > div > span"
        self.team_int_attack_selector = "#list > div:nth-child(4) > div > div > div.column.col-12 > " \
                                        "div > div:nth-child(1) > div > section > div > div:nth-child(2) > div > span"
        self.team_int_midfield_selector = "#list > div:nth-child(4) > div > div > div.column.col-12 > " \
                                          "div > div:nth-child(1) > div > section > div > div:nth-child(3) > div > span"
        self.team_int_defence_selector = "#list > div:nth-child(4) > div > div > div.column.col-12 > " \
                                         "div > div:nth-child(1) > div > section > div > div:nth-child(4) > div > span"
        self.team_int_international_prestige_selector = "#list > div:nth-child(4) > div > div > div.column.col-12 > " \
                                                        "div > div.column.col-4 > div > ul > li:nth-child(3) > span"
        self.team_int_domestic_prestige_selector = "#list > div:nth-child(4) > div > div > div.column.col-12 > " \
                                                   "div > div.column.col-4 > div > ul > li:nth-child(4) > span"
        self.team_int_transfer_budget_selector = "#list > div:nth-child(4) > div > div > " \
                                                 "div.column.col-12 > div > div.column.col-4 > div > ul > " \
                                                 "li:nth-child(5) "

        # tbl_team_tactic
        self.team_str_defensive_style_selector = "#list > div:nth-child(4) > div > div > " \
                                                 "div.column.col-4 > div:nth-child(1) > dl > " \
                                                 "dd:nth-child(2) > span > span "
        self.team_int_team_width_selector = "#list > div:nth-child(4) > div > div > div.column.col-4 > " \
                                            "div:nth-child(1) > dl > dd:nth-child(3) > span.float-right > span"
        self.team_int_depth_selector = "#list > div:nth-child(4) > div > div > div.column.col-4 > " \
                                       "div:nth-child(1) > dl > dd:nth-child(4) > span.float-right > span"
        self.team_str_offensive_style_selector = "#list > div:nth-child(4) > div > " \
                                                 "div > div.column.col-4 > div:nth-child(1) > dl > dd:nth-child(6) > " \
                                                 "span > span "
        self.team_int_width_selector = "#list > div:nth-child(4) > div > div > div.column.col-4 > " \
                                       "div:nth-child(1) > dl > dd:nth-child(7) > span.float-right > span"
        self.team_int_players_in_box_selector = "#list > div:nth-child(4) > div > div > div.column.col-4 > " \
                                                "div:nth-child(1) > dl > dd:nth-child(8) > span.float-right > span"
        self.team_int_corners_selector = "#list > div:nth-child(4) > div > div > div.column.col-4 > " \
                                         "div:nth-child(1) > dl > dd:nth-child(9) > span.float-right > span"
        self.team_int_freekicks_selector = "#list > div:nth-child(4) > div > div > div.column.col-4 > " \
                                           "div:nth-child(1) > dl > dd:nth-child(10) > span.float-right > span"

        # tbl_player

        # use team url for getting the int_team_id
        self.player_str_team_url = "#list > div:nth-child(5) > div > div > div.column.col-12 > div.columns " \
                                   "> div:nth-child(2) > div > div:nth-child(3) > div > h5 > a"
        self.player_str_player_name_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                               "> div.columns > div:nth-child(1) > div > div > h1"
        self.player_str_positions_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                             "> div.columns > div:nth-child(1) > div > div > div > span"
        # text inside div
        self.player_dob_height_weight_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                                 "> div.columns > div:nth-child(1) > div > div > div"
        self.player_int_overall_rating_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                                  "> div.columns > div:nth-child(1) > div > section > div " \
                                                  "> div:nth-child(1) > div > span"
        self.player_int_potential_rating_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                                    "> div.columns > div:nth-child(1) > div > section > div " \
                                                    "> div:nth-child(2) > div > span"
        self.player_str_best_position_selector = "#list > div:nth-child(5) > div > div > div.column.col-4 " \
                                                 "> div.card.calculated > ul > li:nth-child(1) > span"
        self.player_int_best_overall_rating_selector = "#list > div:nth-child(5) > div > div > div.column.col-4 " \
                                                       "> div.card.calculated > ul > li:nth-child(2) > span"
        self.player_int_value_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 > div.columns " \
                                         "> div:nth-child(1) > div > section > div > div:nth-child(3) > div"
        self.player_int_wage_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 > div.columns " \
                                        "> div:nth-child(1) > div > section > div > div:nth-child(4) > div"
        self.player_str_player_image_url_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                                    "> div.columns > div:nth-child(1) > div > img"

        # tbl_player_attacking
        self.player_int_crossing_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 > div.columns " \
                                            "> div:nth-child(4) > div > ul > li:nth-child(1) > span.bp3-tag.p.p-53"
        self.player_int_finishing_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 > div.columns " \
                                             "> div:nth-child(4) > div > ul > li:nth-child(2) > span.bp3-tag.p.p-36"
        self.player_int_heading_accuracy_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                                    "> div.columns > div:nth-child(4) > div > ul " \
                                                    "> li:nth-child(3) > span.bp3-tag.p.p-74"
        self.player_int_short_passing_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                                 "> div.columns > div:nth-child(4) > div > ul > li:nth-child(4) " \
                                                 "> span.bp3-tag.p.p-77"
        self.player_int_volleys_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 > div.columns " \
                                           "> div:nth-child(4) > div > ul > li:nth-child(5) > span.bp3-tag.p.p-42"

        # tbl_player_defending
        self.player_int_defensive_awareness_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                                       "> div.columns > div:nth-child(9) > div > ul " \
                                                       "> li:nth-child(1) > span.bp3-tag.p.p-79"
        self.player_int_standing_tackle_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                                   "> div.columns > div:nth-child(9) > div > ul " \
                                                   "> li:nth-child(2) > span.bp3-tag.p.p-83"
        self.player_int_sliding_tackle_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                                  "> div.columns > div:nth-child(9) > div > ul " \
                                                  "> li:nth-child(3) > span.bp3-tag.p.p-78"

        # tbl_player_goalkeeping
        self.player_int_diving_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                          "> div.columns > div:nth-child(10) > div > ul > li:nth-child(1) > span"
        self.player_int_handling_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 >" \
                                            " div.columns > div:nth-child(10) > div > ul > li:nth-child(2) > span"
        self.player_int_kicking_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                           "> div.columns > div:nth-child(10) > div > ul > li:nth-child(3) > span"
        self.player_int_positioning_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                               "> div.columns > div:nth-child(10) > div > ul > li:nth-child(4) > span"
        self.player_int_reflexes_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                            "> div.columns > div:nth-child(10) > div > ul > li:nth-child(5) > span"

        # tbl_player_mentality
        self.player_int_aggression_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                              "> div.columns > div:nth-child(8) > div > ul " \
                                              "> li:nth-child(1) > span.bp3-tag.p.p-73"
        self.player_int_interceptions_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                                 "> div.columns > div:nth-child(8) > div > ul " \
                                                 "> li:nth-child(2) > span.bp3-tag.p.p-80"
        self.player_int_positioning_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                               "> div.columns > div:nth-child(8) > div > ul " \
                                               "> li:nth-child(3) > span.bp3-tag.p.p-36"
        self.player_int_vision_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                          "> div.columns > div:nth-child(8) > div > ul " \
                                          "> li:nth-child(4) > span.bp3-tag.p.p-67"
        self.player_int_penalties_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                             "> div.columns > div:nth-child(8) > div > ul " \
                                             "> li:nth-child(5) > span.bp3-tag.p.p-40"
        self.player_int_composure_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                             "> div.columns > div:nth-child(8) > div > ul > li:nth-child(6) > span"

        # tbl_player_movement
        self.player_int_acceleration_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                                "> div.columns > div:nth-child(6) > div > ul " \
                                                "> li:nth-child(1) > span.bp3-tag.p.p-73"
        self.player_int_sprint_speed_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                                "> div.columns > div:nth-child(6) > div > ul " \
                                                "> li:nth-child(2) > span.bp3-tag.p.p-81"
        self.player_int_agility_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                           "> div.columns > div:nth-child(6) > div > ul " \
                                           "> li:nth-child(3) > span.bp3-tag.p.p-69"
        self.player_int_reactions_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                             "> div.columns > div:nth-child(6) > div > ul " \
                                             "> li:nth-child(4) > span.bp3-tag.p.p-77"
        self.player_int_balance_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                           "> div.columns > div:nth-child(6) > div > ul " \
                                           "> li:nth-child(5) > span.bp3-tag.p.p-64"

        # tbl_player_power
        self.player_int_shot_power_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                              "> div.columns > div:nth-child(7) > div > ul " \
                                              "> li:nth-child(1) > span.bp3-tag.p.p-75"
        self.player_int_jumping_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                           "> div.columns > div:nth-child(7) > div > ul " \
                                           "> li:nth-child(2) > span.bp3-tag.p.p-80"
        self.player_int_stamina_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                           "> div.columns > div:nth-child(7) > div > ul " \
                                           "> li:nth-child(3) > span.bp3-tag.p.p-72"
        self.player_int_strength_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                            "> div.columns > div:nth-child(7) > div > ul " \
                                            "> li:nth-child(4) > span.bp3-tag.p.p-78"
        self.player_int_long_shots_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                              "> div.columns > div:nth-child(7) > div > ul " \
                                              "> li:nth-child(5) > span.bp3-tag.p.p-48"

        # tbl_player_profile
        self.player_str_preferred_foot_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                                  "> div.columns > div:nth-child(2) > div " \
                                                  "> div:nth-child(1) > div > ul > li:nth-child(1)"
        self.player_int_week_foot_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                             "> div.columns > div:nth-child(2) > div > div:nth-child(1) " \
                                             "> div > ul > li:nth-child(2)"
        self.player_int_skill_moves_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                               "> div.columns > div:nth-child(2) > div > div:nth-child(1) " \
                                               "> div > ul > li:nth-child(3)"
        self.player_int_international_reputations_selector = "#list > div:nth-child(5) > div > div " \
                                                             "> div.column.col-12 > div.columns " \
                                                             "> div:nth-child(2) > div > div:nth-child(1) " \
                                                             "> div > ul > li:nth-child(4)"
        self.player_str_work_rate_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                             "> div.columns > div:nth-child(2) > div > div:nth-child(1) " \
                                             "> div > ul > li:nth-child(5) > span"
        self.player_str_body_type_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                             "> div.columns > div:nth-child(2) > div > div:nth-child(1) " \
                                             "> div > ul > li:nth-child(6) > span"

        # tbl_player_skill
        self.player_int_dribbling_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                             "> div.columns > div:nth-child(5) > div > ul " \
                                             "> li:nth-child(1) > span.bp3-tag.p.p-69"
        self.player_int_curve_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                         "> div.columns > div:nth-child(5) > div > ul " \
                                         "> li:nth-child(2) > span.bp3-tag.p.p-54"
        self.player_int_fk_accuracy_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                               "> div.columns > div:nth-child(5) > div > ul " \
                                               "> li:nth-child(3) > span.bp3-tag.p.p-55"
        self.player_int_long_passing_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                                "> div.columns > div:nth-child(5) > div > ul " \
                                                "> li:nth-child(4) > span.bp3-tag.p.p-74"
        self.player_int_ball_control_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                                "> div.columns > div:nth-child(5) > div > ul " \
                                                "> li:nth-child(5) > span.bp3-tag.p.p-74"

        # tbl_player_specialities, extract from list
        self.player_str_player_speciality_selector = "#list > div:nth-child(5) > div > div " \
                                                     "> div.column.col-12 > div.columns > div:nth-child(2) " \
                                                     "> div > div:nth-child(2) > div > ul"

        # tbl_player_traits, extract from list
        self.player_str_trait_selector = "#list > div:nth-child(5) > div > div > div.column.col-12 " \
                                         "> div.columns > div:nth-child(11) > div > ul"

    def handle_tbl_team(self, soup, tbl_team_url):
        """ Extracts information about tbl_team and returns """
        tbl_team = TblTeam()
        tbl_team.int_team_id = tbl_team_url.int_team_id
        tbl_team.str_team_name = soup.select(self.team_str_team_name_selector)[0].text
        tbl_team.str_league = soup.select(self.team_str_league_selector)[0].text
        tbl_team.int_overall = int(soup.select(self.team_int_overall_selector)[0].text)
        tbl_team.int_attack = int(soup.select(self.team_int_attack_selector)[0].text)
        tbl_team.int_midfield = int(soup.select(self.team_int_midfield_selector)[0].text)
        tbl_team.int_defence = int(soup.select(self.team_int_defence_selector)[0].text)
        tbl_team.int_international_prestige = int(soup.select(self.team_int_international_prestige_selector)
                                                  [0].text)
        tbl_team.int_domestic_prestige = int(soup.select(self.team_int_domestic_prestige_selector)[0].text)

        str_transfer_budget = soup.select(self.team_int_transfer_budget_selector)[0].text
        int_transfer_budget = self.format_money(str_transfer_budget)

        if int_transfer_budget is not None:
            tbl_team.int_transfer_budget = int_transfer_budget

        return tbl_team

    def handle_tbl_team_tactics(self, soup, tbl_team_url):

        tbl_team_tactic = TblTeamTactic()
        tbl_team_tactic.int_team_id = tbl_team_url.int_team_id
        tbl_team_tactic.str_defensive_style = soup.select(self.team_str_defensive_style_selector)[0].text
        tbl_team_tactic.int_team_width = int(soup.select(self.team_int_team_width_selector)[0].text)
        tbl_team_tactic.int_depth = int(soup.select(self.team_int_depth_selector)[0].text)
        tbl_team_tactic.str_offensive_style = soup.select(self.team_str_offensive_style_selector)[0].text
        tbl_team_tactic.int_width = int(soup.select(self.team_int_width_selector)[0].text)
        tbl_team_tactic.int_players_in_box = int(soup.select(self.team_int_players_in_box_selector)[0].text)
        tbl_team_tactic.int_corners = int(soup.select(self.team_int_corners_selector)[0].text)
        tbl_team_tactic.int_freekicks = int(soup.select(self.team_int_freekicks_selector)[0].text)

        return tbl_team_tactic

    def handle_tbl_player(self, soup, int_team_id):
        tbl_player = TblPlayer()
        tbl_player.int_team_id = int_team_id
        tbl_player.str_player_name = soup.select(self.player_str_player_name_selector)[0].text
        tbl_player.str_positions = soup.select(self.player_str_positions_selector)[0].text

        dob_height_weight = soup.select(self.player_dob_height_weight_selector)[0].text
        dob, height, weight = self.split_personal_data(dob_height_weight)

        if height is not None:
            try:
                tbl_player.int_height = int(height)
            except ValueError:
                print("Error while converting height to int value")

        if weight is not None:
            try:
                tbl_player.int_weight = int(weight)
            except ValueError:
                print("Error while converting weight to int value")

        if dob is not None:
            date_of_birth = self.parse_date(dob)
            tbl_player.dt_date_of_birth = date_of_birth

        tbl_player.int_overall_rating = int(soup.select(self.team_int_overall_selector)[0].text)
        tbl_player.int_potential_rating = int(soup.select(self.player_int_potential_rating_selector)[0].text)
        tbl_player.str_best_position = soup.select(self.player_str_best_position_selector)[0].text
        tbl_player.int_best_overall_rating = int(soup.select(self.player_int_best_overall_rating_selector)[0].text)

        str_value = soup.select(self.player_int_value_selector)[0].text
        int_value = self.format_money(str_value)

        if int_value is not None:
            tbl_player.int_value = int_value

        str_wage = soup.select(self.player_int_wage_selector)[0].text
        int_wage = self.format_money(str_wage)

        if int_wage is not None:
            tbl_player.int_wage = int_wage

        tbl_player.str_player_image_url = soup.select(self.player_str_player_image_url_selector)[0].text

    def handle_tbl_player_attacking(self, soup, int_player_id):
        pass

    def handle_tbl_player_defending(self, soup, int_player_id):
        pass

    def handle_tbl_player_goalkeeping(self, soup, int_player_id):
        pass

    def handle_tbl_player_mentality(self, soup, int_player_id):
        pass

    def handle_tbl_player_movement(self, soup, int_player_id):
        pass

    def handle_tbl_player_power(self, soup, int_player_id):
        pass

    def handle_tbl_player_profile(self, soup, int_player_id):
        pass

    def handle_tbl_player_skill(self, soup, int_player_id):
        pass

    def handle_tbl_player_specialities(self, soup, int_player_id):
        pass

    def handle_tbl_player_traits(self, soup, int_player_id):
        pass

    @staticmethod
    def format_money(money):

        money = money.split("€")[1]  # Remove "Transfer Budget text
        money = money.replace(".", "")  # Remove dots

        if money.endswith("M"):
            money = money[:-1] + "000000"  # Remove M and add 6 zeros
        elif money.endswith("K"):
            money = money[:-1] + "000"  # Remove K and add 3 zeros
        else:
            print(money)

        try:
            return int(money)
        except ValueError:
            return None

    @staticmethod
    def split_personal_data(personal_data_text):

        regex = r"(\()(.*?)(\))( )(\d{3})(cm )(.*?)(kg)"

        matches = re.search(regex, personal_data_text)

        if matches:
            return matches.group(2), matches.group(5), matches.group(7)
        else:
            return None, None, None

    @staticmethod
    def parse_date(date):
        # TODO
        return date
