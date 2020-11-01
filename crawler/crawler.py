from requests import get
from bs4 import BeautifulSoup
from time import sleep


class Crawler:
    """ Gathers team and player urls and extracts information about them """

    # delay, sec
    politeness = 2

    base_site_url = "https://sofifa.com"
    next_page_selector = "#adjust > div > div.column.col-auto > div > div > a"

    # team selectors
    base_teams_url = "https://sofifa.com/teams?type=club"
    teams_url_selector = "#adjust > div > div.column.col-auto > div > " \
                         "table > tbody > tr > td.col-name-wide > a:nth-child(1)"

    team_urls = []

    # player selectors
    base_player_url = "https://sofifa.com/players?r=210007&set=true"
    players_next_page_selector = "#adjust > div > div.column.col-auto > div > div > a"
    player_url_selector = "#adjust > div > div.column.col-auto > div > table > " \
                          "tbody > tr > td > a.tooltip"
    player_urls = []

    def crawl_teams(self):

        try:

            current_page = self.base_teams_url
            is_next_page_exists = True

            while is_next_page_exists:
                response = get(current_page)
                print("Current page: " + current_page)
                soup = BeautifulSoup(response.text, 'html.parser')

                self.get_team_urls_in_page(soup)
                print(str(len(self.team_urls)) + " team link found so far.")

                # check if next page exists before going to the next page
                is_next_page_exists, current_page = self.is_next_page_exists(soup)
                current_page = self.base_site_url + current_page

                sleep(self.politeness)

        except Exception as e:
            print(e)

        print("All links found.")
        # TODO visit_team_page()

    def crawl_players(self):
        try:

            current_page = self.base_player_url
            is_next_page_exists = True

            while is_next_page_exists:
                response = get(current_page)
                print("Current page: " + current_page)
                soup = BeautifulSoup(response.text, 'html.parser')

                self.get_player_urls_in_page(soup)
                print(str(len(self.player_urls)) + " player link found so far.")

                # check if next page exists before going to the next page
                is_next_page_exists, current_page = self.is_next_page_exists(soup)
                current_page = self.base_site_url + current_page

                sleep(self.politeness)

        except Exception as e:
            print(e)

        print("All links found.")
        # TODO visit_player_page()

    def visit_team_page(self):
        pass

    def visit_player_page(self):
        pass

    def get_team_urls_in_page(self, soup):
        """ Finds team url in current page and added to the team_urls list """
        team_urls_in_page = soup.select(self.teams_url_selector)

        for url in team_urls_in_page:
            self.team_urls.append(self.base_site_url + url["href"])

    def get_player_urls_in_page(self, soup):
        """ Finds player url in current page and added to the player_urls list """
        player_urls_in_page = soup.select(self.player_url_selector)

        for url in player_urls_in_page:
            self.player_urls.append(self.base_site_url + url["href"])

    def is_next_page_exists(self, soup):
        """ Returns if next page button exists, and if it's exists returns url of the next page also. """

        next_page = soup.select(self.next_page_selector)

        for buttons in next_page:
            if buttons.text == "Next":
                return True, buttons["href"]
        return False, ""

