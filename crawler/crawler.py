from requests import get  # main tool for getting the page source
import shutil  # to save image locally
from bs4 import BeautifulSoup  # html parser
from time import sleep
from controllers.controllers import Controllers
from crawler.crawler_utils import CrawlerUtils
import logging


class Crawler:
    """
    Gathers team and player urls, visit those urls and extracts information in them
    """

    def __init__(self):

        self.logger = logging.getLogger("sLogger")

        # DB controller
        self.controller = Controllers()

        # Crawler Utils
        self.crawler_utils = CrawlerUtils()

        # delay sec, be kind to the server
        self.politeness = 1

        # lists that stores pages to be crawl
        self.team_urls = []
        self.player_urls = []

        # team tables
        self.teams = []
        self.team_tactics = []

        # player tables
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

        self.base_site_url = "https://sofifa.com"
        self.next_page_selector = "#adjust > div > div.column.col-auto > div > div > a"

        # team selectors
        self.base_teams_url = "https://sofifa.com/teams?type=club"
        self.teams_url_selector = "#adjust > div > div.column.col-auto > div > " \
                                  "table > tbody > tr > td.col-name-wide > a:nth-child(1)"

        # player selectors
        self.base_players_url = "https://sofifa.com/players?r=210007&set=true"
        self.players_next_page_selector = "#adjust > div > div.column.col-auto > div > div > a"
        self.player_url_selector = "#adjust > div > div.column.col-auto > div > table > " \
                                   "tbody > tr > td > a.tooltip"

    def crawl(self):

        # Team url crawling and inserting
        self.gather_links(is_team=True)  # default is True but pass it anyway
        self.controller.insert_tbl_team_urls(self.team_urls)

        self.logger.info("Team urls inserted to DB.")

        self.logger.info("Team pages crawling started.")
        self.visit_team_page(controller=self.controller)
        self.controller.insert_tbl_team(tbl_teams=self.teams)
        self.controller.insert_tbl_team_tactic(tbl_team_tactics=self.team_tactics)
        self.logger.info("Team pages crawling finished.")

        # Player url crawling and inserting
        self.gather_links(is_team=False)
        self.controller.insert_tbl_player_urls(self.player_urls)

        self.logger.info("Player urls inserted to DB")

        self.logger.info("Player pages crawling started.")
        self.visit_player_page(controller=self.controller)
        self.logger.info("Player pages crawling finished.")

        self.logger.info("Player's images crawling started.")
        self.download_player_image()
        self.logger.info("Player's images crawling finished.")

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
                self.logger.info("Current page: " + current_page)
                soup = BeautifulSoup(response.text, 'html.parser')

                if is_team:
                    self.get_urls_in_page(soup, is_team=True)  # default is True but pass it anyway
                    self.logger.debug(str(len(self.team_urls)) + " team link found so far.")
                else:
                    self.get_urls_in_page(soup, is_team=False)
                    self.logger.debug(str(len(self.player_urls)) + " player link found so far.")

                # check if next page exists before going to the next page
                is_next_page_exists, current_page = self.is_next_page_exists(soup)
                current_page = self.base_site_url + current_page

                sleep(self.politeness)

        except Exception as e:
            self.logger.exception(e)

        self.logger.info("All links found.")

    def get_urls_in_page(self, soup, is_team=True):
        """
        Takes is_team as a parameter, according to that it collects appropriate urls and stores for crawling later
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

    def visit_team_page(self):
        """ Visits a url and extract information about teams """

        tbl_team_urls = self.controller.get_tbl_team_urls()

        for i, tbl_team_url in enumerate(tbl_team_urls):

            response = get(tbl_team_url.str_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            tbl_team = self.crawler_utils.handle_tbl_team(soup=soup, tbl_team_url=tbl_team_url)
            self.teams.append(tbl_team)

            tbl_team_tactic = self.crawler_utils.handle_tbl_team_tactics(soup=soup, tbl_team_url=tbl_team_url)
            self.team_tactics.append(tbl_team_tactic)

            self.logger.info("{}/{} - {} crawled".format(i + 1, len(tbl_team_urls), tbl_team.str_team_name))
            sleep(self.politeness)

    def visit_player_page(self):
        """ Visit a url and extract information about players """

        # add ?units=mks to url to get correct units
        metric = "?units=mks"

        tbl_player_urls = self.controller.get_tbl_player_urls()

        # Get 250 player url every time
        while len(tbl_player_urls) != 0:
            self.logger.info("New player batch started.")
            for i, tbl_player_url in enumerate(tbl_player_urls):

                response = get(tbl_player_url.str_url + metric)
                soup = BeautifulSoup(response.text, 'html.parser')

                int_player_id = tbl_player_url.int_player_id

                # get team url
                if len(soup.select(self.crawler_utils.player_str_team_url)) >= 1:
                    str_team_url = soup.select(self.crawler_utils.player_str_team_url)[0]["href"]
                    str_team_url = self.base_site_url + str_team_url

                # get team id from url -if exists-
                int_team_id = self.controller.get_team_id_by_url(str_team_url)

                # Sometimes website lists team and national team url's mixed order.
                # If team url not found in DB then probably we get national team's url.
                if int_team_id is None:
                    if len(soup.select(self.crawler_utils.player_str_national_team_url)) >= 1:
                        str_team_url = soup.select(self.crawler_utils.player_str_national_team_url)[0]["href"]
                        str_team_url = self.base_site_url + str_team_url
                        int_team_id = self.controller.get_team_id_by_url(str_team_url)

                # If we still can not find the team url, probably current player has no team.
                if int_team_id is None:
                    int_team_id = 'NULL'

                tbl_player = self.crawler_utils.handle_tbl_player(soup=soup,
                                                                  int_player_id=int_player_id,
                                                                  int_team_id=int_team_id)

                self.players.append(tbl_player)

                # Attacking
                tbl_player_attacking = self.crawler_utils.handle_tbl_player_attacking(soup=soup,
                                                                                      int_player_id=int_player_id)
                self.player_attacking.append(tbl_player_attacking)

                # Defending
                tbl_player_defending = self.crawler_utils.handle_tbl_player_defending(soup=soup,
                                                                                      int_player_id=int_player_id)
                self.player_defending.append(tbl_player_defending)

                # Goalkeeping
                tbl_player_goalkeeping = self.crawler_utils.handle_tbl_player_goalkeeping(soup=soup,
                                                                                          int_player_id=int_player_id)
                self.player_goalkeeping.append(tbl_player_goalkeeping)

                # Mentality
                tbl_player_mentality = self.crawler_utils.handle_tbl_player_mentality(soup=soup,
                                                                                      int_player_id=int_player_id)
                self.player_mentality.append(tbl_player_mentality)

                # Movement
                tbl_player_movement = self.crawler_utils.handle_tbl_player_movement(soup=soup,
                                                                                    int_player_id=int_player_id)
                self.player_movement.append(tbl_player_movement)

                # Power
                tbl_player_power = self.crawler_utils.handle_tbl_player_power(soup=soup,
                                                                              int_player_id=int_player_id)
                self.player_power.append(tbl_player_power)

                # Profile
                tbl_player_profile = self.crawler_utils.handle_tbl_player_profile(soup=soup,
                                                                                  int_player_id=int_player_id)
                self.player_profile.append(tbl_player_profile)

                # Skill
                tbl_player_skill = self.crawler_utils.handle_tbl_player_skill(soup=soup,
                                                                              int_player_id=int_player_id)
                self.player_skill.append(tbl_player_skill)

                # Specialities
                tbl_player_speciality = self.crawler_utils.handle_tbl_player_specialities(soup=soup,
                                                                                          int_player_id=int_player_id)
                self.player_speciality.append(tbl_player_speciality)

                # Traits
                tbl_player_traits = self.crawler_utils.handle_tbl_player_traits(soup=soup,
                                                                                int_player_id=int_player_id)
                self.player_traits.append(tbl_player_traits)

                self.logger.debug("{}/{} - {} crawled".format(i + 1, len(tbl_player_urls), tbl_player.str_player_name))
                sleep(self.politeness)

            # Handle inserting operations after 250 player loop finishes
            self.handle_insert_player_tables()
            self.logger.info("Current player batch finished.")
            tbl_player_urls = self.controller.get_tbl_player_urls()  # Get new batch

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

    def download_player_image(self):
        """ This function saves player images """

        images_folder_path = "./data/images/"
        tbl_player_image_urls = self.controller.get_tbl_player_image_urls()

        for tbl_player in tbl_player_image_urls:
            image_path = images_folder_path + str(tbl_player.int_player_id) + ".png"
            r = get(tbl_player.str_player_image_url, stream=True)

            # Check if the image was retrieved successfully
            if r.status_code == 200:

                # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                r.raw.decode_content = True

                # Open a local file with wb (write binary) permission.
                with open(image_path, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)

                self.logger.debug('Player ID: %s image successfully downloaded: ', str(tbl_player.int_player_id))
                sleep(self.politeness)
            else:
                self.logger.debug('Player ID: %s Status Code: %s image could not retrieved',
                                  str(tbl_player.int_player_id),
                                  str(r.status_code))
