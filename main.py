from crawler.crawler import Crawler
import sys
from datetime import datetime
import logging
import logging.config


def main():

    logging.config.fileConfig("logging.conf")
    logger = logging.getLogger("sLogger")
    logger.info("Crawling started at: " + datetime.now().strftime("%H:%M:%S"))

    crawler = Crawler()
    crawler.crawl()
    logger.info("Crawling ended at: " + datetime.now().strftime("%H:%M:%S"))

    sys.exit()


if __name__ == '__main__':
    main()
