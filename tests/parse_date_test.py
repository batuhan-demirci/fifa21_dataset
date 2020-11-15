from datetime import datetime
import logging

logger = logging.getLogger("sLogger")


def parse_date(date):
    date_object = datetime.strptime(date, "%b %d, %Y")
    return date_object


def test():

    str_date = "Jun 2, 1987"
    dt_date = parse_date(str_date)
    logger.debug(dt_date)
    logger.debug("Başakşehİr")
