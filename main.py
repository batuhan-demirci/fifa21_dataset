from crawler.crawler import Crawler
# from controllers.controllers import Controllers

# TODO logging

if __name__ == '__main__':
    crawler = Crawler()
    crawler.crawl()

    # controller = Controllers()
    # controller.get_team_id_by_url("https://sofifa.com/team/21/fc-bayern-munchen/")
