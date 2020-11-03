# from utils.db_connection_manager import ConnectionManager
# from models.models import TblTeamUrl
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from utils.db_connection_manager import ConnectionManager
from crawler.crawler import Crawler

# TODO logging

if __name__ == '__main__':

    crawler = Crawler()

    crawler.gather_links(is_team=True)  # default is True but pass it anyway
    crawler.gather_links(is_team=False)

    # crawler.crawl_teams()
    # crawler.crawl_players()

    # TODO visit_team_page()
    # TODO visit_player_page()

    # db_manager = ConnectionManager()
    # connection, cursor = db_manager.connect()

    # engine = create_engine(db_manager.get_connection_string())

    # Session = sessionmaker(bind=engine)
    # s = Session()

    # stuff
    # team = TblTeamUrl()
    # team.int_team_id = 1
    # team.str_url = "as123"

    # s.add(team)
    # s.commit()

    # s.close_all()

    # cursor.execute("SELECT version();")
    # rows = cursor.fetchall()

    # for row in rows:
    #    print(row)

    # db_manager.close(connection, cursor)
