from requests import get
from bs4 import BeautifulSoup
from time import sleep
from controllers.controllers import Controllers
from models.models import TblTeam, TblTeamTactic


class Crawler:
    """
    Gathers team and player urls, visit those urls and extracts information in them
    """

    # delay sec, be kind to the server
    politeness = 2

    # lists that stores pages to be crawl
    team_urls = []
    player_urls = []

    # team tables
    teams = []
    team_tactics = []

    base_site_url = "https://sofifa.com"
    next_page_selector = "#adjust > div > div.column.col-auto > div > div > a"

    # team selectors
    base_teams_url = "https://sofifa.com/teams?type=club"
    teams_url_selector = "#adjust > div > div.column.col-auto > div > " \
                         "table > tbody > tr > td.col-name-wide > a:nth-child(1)"

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

    # player selectors
    base_players_url = "https://sofifa.com/players?r=210007&set=true"
    players_next_page_selector = "#adjust > div > div.column.col-auto > div > div > a"
    player_url_selector = "#adjust > div > div.column.col-auto > div > table > " \
                          "tbody > tr > td > a.tooltip"

    def crawl(self):

        controller = Controllers()

        # Team url crawling and inserting
        # self.gather_links(is_team=True)  # default is True but pass it anyway
        # controller.insert_tbl_team_urls(self.team_urls)

        # print("Team urls inserted to DB.")

        self.visit_team_page(controller=controller)
        # controller.insert_tbl_team(tbl_teams=self.teams)
        controller.insert_tbl_team_tactic(tbl_team_tactics=self.team_tactics)

        # Player url crawling and inserting
        # self.gather_links(is_team=False)
        # controller.insert_tbl_player_urls(self.player_urls)

        # print("Player urls inserted to DB")

    def gather_links(self, is_team=True):
        """
        Takes is_team as a parameter and according to that gather links for teams or players
        At each page it checks if there is a next page, and if so continues to the next page as well.
        """
        try:

            current_page = self.base_teams_url if is_team else self.base_players_url
            is_next_page_exists = True

            while is_next_page_exists:
                response = get(current_page)
                print("Current page: " + current_page)
                soup = BeautifulSoup(response.text, 'html.parser')

                if is_team:
                    self.get_urls_in_page(soup, is_team=True)  # default is True but pass it anyway
                    print(str(len(self.team_urls)) + " team link found so far.")
                else:
                    self.get_urls_in_page(soup, is_team=False)
                    print(str(len(self.player_urls)) + " player link found so far.")

                # check if next page exists before going to the next page
                is_next_page_exists, current_page = self.is_next_page_exists(soup)
                current_page = self.base_site_url + current_page

                sleep(self.politeness)

        except Exception as e:
            # TODO needs handling
            print(e)

        print("All links found.")

    def get_urls_in_page(self, soup, is_team=True):
        """
        Takes is_team as a parameter, according to that it collects appropriate urls and stores
        """

        if is_team:
            team_urls_in_page = soup.select(self.teams_url_selector)
            for url in team_urls_in_page:
                self.team_urls.append(self.base_site_url + url["href"])
        else:
            player_urls_in_page = soup.select(self.player_url_selector)
            for url in player_urls_in_page:
                self.player_urls.append(self.base_site_url + url["href"])

    def is_next_page_exists(self, soup):
        """
        Returns if next page button exists, and if it's exists returns url of the next page also.
        """

        next_page = soup.select(self.next_page_selector)

        for buttons in next_page:
            if buttons.text == "Next":
                return True, buttons["href"]
        return False, ""

    def visit_team_page(self, controller):
        tbl_team_urls = controller.get_tbl_team_urls()

        for tbl_team_url in tbl_team_urls:
            response = get(tbl_team_url.str_url)
            soup = BeautifulSoup(response.text, 'html.parser')

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

            self.teams.append(tbl_team)

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

            self.team_tactics.append(tbl_team_tactic)

            print("{} crawled".format(tbl_team.str_team_name))
            sleep(self.politeness)

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


    def visit_player_page(self):
        pass
