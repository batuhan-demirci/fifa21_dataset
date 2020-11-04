from utils.db_connection_manager import ConnectionManager
from controllers.controllers import Controllers
from models.models import TblTeamUrl


with ConnectionManager() as manager:
    tbl_team_url = TblTeamUrl()
    tbl_team_url.str_url = "testing.com"

    manager.cur.execute(Controllers.insert_tbl_team_urls.format(tbl_team_url.str_url, tbl_team_url.dt_crawled))
    manager.con.commit()
