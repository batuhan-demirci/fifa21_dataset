from crawler.crawler import Crawler
import sys
from datetime import datetime
from controllers.controllers import Controllers

# TODO logging

if __name__ == '__main__':

    print("Crawling started at: ", datetime.now().strftime("%H:%M:%S"))

    # crawler = Crawler()
    # crawler.crawl()

    print("Crawling ended at: ", datetime.now().strftime("%H:%M:%S"))

    # sys.exit()

    controller = Controllers()
    int_team_id = controller.get_team_id_by_url("https://sofifa.com/team/241/fc-barcelona/")
    if int_team_id is None:
        print("not found")
    else:
        print(int_team_id)
