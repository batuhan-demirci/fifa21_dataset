from requests import get
from bs4 import BeautifulSoup
from time import sleep
from controllers.controllers import Controllers
from crawler.crawler_utils import CrawlerUtils


class Crawler:
    """
    Gathers team and player urls, visit those urls and extracts information in them
    """

    # DB controller
    controller = Controllers()

    # delay sec, be kind to the server
    politeness = 2

    # lists that stores pages to be crawl
    team_urls = []
    player_urls = []

    # team tables
    teams = []
    team_tactics = []

    # player tables
    players = []
    player_attacking = []
    player_defending = []
    player_goalkeeping = []
    player_mentality = []
    player_movement = []
    player_power = []
    player_profile = []
    player_skill = []
    player_speciality = []
    player_traits = []

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

        # Team url crawling and inserting
        # self.gather_links(is_team=True)  # default is True but pass it anyway
        # controller.insert_tbl_team_urls(self.team_urls)

        # print("Team urls inserted to DB.")

        # self.visit_team_page(controller=controller)
        # controller.insert_tbl_team(tbl_teams=self.teams)
        # controller.insert_tbl_team_tactic(tbl_team_tactics=self.team_tactics)

        # Player url crawling and inserting
        # self.gather_links(is_team=False)
        # controller.insert_tbl_player_urls(self.player_urls)
        self.visit_player_page(controller=self.controller)
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

        for i, tbl_team_url in enumerate(tbl_team_urls):
            response = get(tbl_team_url.str_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            tbl_team = CrawlerUtils.handle_tbl_team(soup=soup, tbl_team_url=tbl_team_url)
            self.teams.append(tbl_team)

            tbl_team_tactic = CrawlerUtils.handle_tbl_team_tactics(soup=soup, tbl_team_url=tbl_team_url)
            self.team_tactics.append(tbl_team_tactic)

            print("{}/{} - {} crawled".format(i + 1, len(tbl_team_urls), tbl_team.str_team_name))
            sleep(self.politeness)

    def visit_player_page(self, controller):
        tbl_player_urls = controller.get_tbl_player_urls()

        while len(tbl_player_urls) != 0:
            for i, tbl_player_url in enumerate(tbl_player_urls):
                response = get(tbl_player_url.str_url)
                soup = BeautifulSoup(response.text, 'html.parser')

                tbl_player = CrawlerUtils.handle_tbl_player(soup=soup)
                self.players.append(tbl_player)

                int_player_id = tbl_player.int_player_id

                # Attacking
                tbl_player_attacking = CrawlerUtils.handle_tbl_player_attacking(soup=soup,
                                                                                int_player_id=int_player_id)
                self.player_attacking.append(tbl_player_attacking)

                # Defending
                tbl_player_defending = CrawlerUtils.handle_tbl_player_defending(soup=soup,
                                                                                int_player_id=int_player_id)
                self.player_defending.append(tbl_player_defending)

                # Goalkeeping
                tbl_player_goalkeeping = CrawlerUtils.handle_tbl_player_goalkeeping(soup=soup,
                                                                                    int_player_id=int_player_id)
                self.player_goalkeeping.append(tbl_player_goalkeeping)

                # Mentality
                tbl_player_mentality = CrawlerUtils.handle_tbl_player_mentality(soup=soup,
                                                                                int_player_id=int_player_id)
                self.player_mentality.append(tbl_player_mentality)

                # Movement
                tbl_player_movement = CrawlerUtils.handle_tbl_player_movement(soup=soup,
                                                                              int_player_id=int_player_id)
                self.player_movement.append(tbl_player_movement)

                # Power
                tbl_player_power = CrawlerUtils.handle_tbl_player_power(soup=soup,
                                                                        int_player_id=int_player_id)
                self.player_power.append(tbl_player_power)

                # Profile
                tbl_player_profile = CrawlerUtils.handle_tbl_player_profile(soup=soup,
                                                                            int_player_id=int_player_id)
                self.player_profile.append(tbl_player_profile)

                # Skill
                tbl_player_skill = CrawlerUtils.handle_tbl_player_skill(soup=soup,
                                                                        int_player_id=int_player_id)
                self.player_skill.append(tbl_player_skill)

                # Specialities
                tbl_player_speciality = CrawlerUtils.handle_tbl_player_specialities(soup=soup,
                                                                                    int_player_id=int_player_id)
                self.player_speciality.append(tbl_player_speciality)

                # Traits
                tbl_player_traits = CrawlerUtils.handle_tbl_player_traits(soup=soup,
                                                                          int_player_id=int_player_id)
                self.player_traits.append(tbl_player_traits)

                print("{}/{} - {} crawled".format(i + 1, len(tbl_player_urls), tbl_player.str_player_name))
                sleep(self.politeness)

            # Handle inserting operations after 500 player loop finishes
            self.handle_insert_player_tables()

    def handle_insert_player_tables(self):
        """ Inserts and clears player tables """
        self.controller.insert_tbl_player(self.players)
        self.controller.insert_tbl_player_attacking(self.player_attacking)
        self.controller.insert_tbl_player_defending(self.player_defending)
        self.controller.insert_tbl_player_goalkeeping(self.player_goalkeeping)
        self.controller.insert_tbl_player_mentality(self.player_mentality)
        self.controller.insert_tbl_player_movement(self.player_movement)
        self.controller.insert_tbl_player_power(self.player_power)
        self.controller.insert_tbl_player_profile(self.player_profile)
        self.controller.insert_tbl_player_skill(self.player_skill)
        self.controller.insert_tbl_player_speciality(self.player_speciality)
        self.controller.insert_tbl_player_traits(self.player_traits)

        self.players = []
        self.player_attacking = []
        self.player_defending = []
        self.player_goalkeeping = []
        self.player_mentality = []
        self.player_movement = []
        self.player_power = []
        self.player_profile = []
        self.player_skill = []
        self.player_speciality = []
        self.player_traits = []
