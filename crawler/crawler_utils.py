from models.models import TblTeam, TblTeamTactic


class CrawlerUtils:

    team_str_team_name_selector = "#list > div:nth-child(4) > div > div > div.column.col-12 > div > " \
                                  "div:nth-child(1) > div > div > h1"
    team_str_league_selector = "#list > div:nth-child(4) > div > div > div.column.col-12 > div > " \
                               "div:nth-child(1) > div > div > div > a:nth-child(2)"
    team_int_overall_selector = "#list > div:nth-child(4) > div > div > div.column.col-12 > div > " \
                                "div:nth-child(1) > div > section > div > div:nth-child(1) > div > span"
    team_int_attack_selector = "#list > div:nth-child(4) > div > div > div.column.col-12 > " \
                               "div > div:nth-child(1) > div > section > div > div:nth-child(2) > div > span"
    team_int_midfield_selector = "#list > div:nth-child(4) > div > div > div.column.col-12 > " \
                                 "div > div:nth-child(1) > div > section > div > div:nth-child(3) > div > span"
    team_int_defence_selector = "#list > div:nth-child(4) > div > div > div.column.col-12 > " \
                                "div > div:nth-child(1) > div > section > div > div:nth-child(4) > div > span"
    team_int_international_prestige_selector = "#list > div:nth-child(4) > div > div > div.column.col-12 > " \
                                               "div > div.column.col-4 > div > ul > li:nth-child(3) > span"
    team_int_domestic_prestige_selector = "#list > div:nth-child(4) > div > div > div.column.col-12 > " \
                                          "div > div.column.col-4 > div > ul > li:nth-child(4) > span"
    team_int_transfer_budget_selector = "#list > div:nth-child(4) > div > div > " \
                                        "div.column.col-12 > div > div.column.col-4 > div > ul > li:nth-child(5)"
    team_str_defensive_style_selector = "#list > div:nth-child(4) > div > div > " \
                                        "div.column.col-4 > div:nth-child(1) > dl > dd:nth-child(2) > span > span"
    team_int_team_width_selector = "#list > div:nth-child(4) > div > div > div.column.col-4 > " \
                                   "div:nth-child(1) > dl > dd:nth-child(3) > span.float-right > span"
    team_int_depth_selector = "#list > div:nth-child(4) > div > div > div.column.col-4 > " \
                              "div:nth-child(1) > dl > dd:nth-child(4) > span.float-right > span"
    team_str_offensive_style_selector = "#list > div:nth-child(4) > div > " \
                                        "div > div.column.col-4 > div:nth-child(1) > dl > dd:nth-child(6) > span > span"
    team_int_width_selector = "#list > div:nth-child(4) > div > div > div.column.col-4 > " \
                              "div:nth-child(1) > dl > dd:nth-child(7) > span.float-right > span"
    team_int_players_in_box_selector = "#list > div:nth-child(4) > div > div > div.column.col-4 > " \
                                       "div:nth-child(1) > dl > dd:nth-child(8) > span.float-right > span"
    team_int_corners_selector = "#list > div:nth-child(4) > div > div > div.column.col-4 > " \
                                "div:nth-child(1) > dl > dd:nth-child(9) > span.float-right > span"
    team_int_freekicks_selector = "#list > div:nth-child(4) > div > div > div.column.col-4 > " \
                                  "div:nth-child(1) > dl > dd:nth-child(10) > span.float-right > span"

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
        int_transfer_budget = self.format_transfer_budget(str_transfer_budget)

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

    def handle_tbl_player(self, soup):
        pass

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
    def format_transfer_budget(str_transfer_budget):

        str_transfer_budget = str_transfer_budget.split("€")[1]  # Remove "Transfer Budget text
        str_transfer_budget = str_transfer_budget.replace(".", "")  # Remove dots

        if str_transfer_budget.endswith("M"):
            str_transfer_budget = str_transfer_budget[:-1] + "000000"  # Remove M and add 6 zeros
        elif str_transfer_budget.endswith("K"):
            str_transfer_budget = str_transfer_budget[:-1] + "000"  # Remove K and add 3 zeros
        else:
            print(str_transfer_budget)

        try:
            return int(str_transfer_budget)
        except ValueError:
            return None
