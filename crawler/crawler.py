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
    base_players_url = "https://sofifa.com/players?r=210007&set=true"
    players_next_page_selector = "#adjust > div > div.column.col-auto > div > div > a"
    player_url_selector = "#adjust > div > div.column.col-auto > div > table > " \
                          "tbody > tr > td > a.tooltip"
    player_urls = []

    def gather_links(self, is_team=True):
        """ This function crawl team or player pages and gather links """
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
        """ Collects team or player links """

        if is_team:
            team_urls_in_page = soup.select(self.teams_url_selector)
            for url in team_urls_in_page:
                self.team_urls.append(self.base_site_url + url["href"])
        else:
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

    def visit_team_page(self):
        pass

    def visit_player_page(self):
        pass
