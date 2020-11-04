from crawler.crawler import Crawler
from utils.db_connection_manager import ConnectionManager
from controllers.controllers import Controllers
from models.models import TblTeamUrl

# TODO logging

if __name__ == '__main__':

    crawler = Crawler()

    crawler.gather_links(is_team=True)  # default is True but pass it anyway

    with ConnectionManager() as manager:
        for team_url in crawler.team_urls:
            tbl_team_url = TblTeamUrl()
            tbl_team_url.str_url = team_url

            manager.cur.execute(Controllers.insert_tbl_team_urls.format(tbl_team_url.str_url, tbl_team_url.dt_crawled))
            manager.con.commit()

    # crawler.gather_links(is_team=False)

    # crawler.crawl_teams()
    # crawler.crawl_players()

    crawler.visit_team_page()
    # TODO crawler.visit_player_page()


#         db_manager = ConnectionManager()
#         connection, cursor = db_manager.connect()
#
#         engine = create_engine(db_manager.get_connection_string())
#
#         Session = sessionmaker(bind=engine)
#         # s = Session()
#
#         # stuff
#         # team = TblTeamUrl()
#         # team.int_team_id = 1
#         # team.str_url = "as123"
#
#         # s.add(team)
#         # s.commit()
#
#         # s.close_all()
#
#         # cursor.execute("SELECT version();")
#         # rows = cursor.fetchall()
#
#         # for row in rows:
#         #    print(row)
#
#         # db_manager.close(connection, cursor)