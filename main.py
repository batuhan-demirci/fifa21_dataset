from crawler.crawler import Crawler
import sys
import logging
import logging.config
from utils import generate_data


def main():

    logging.config.fileConfig("logging.conf")
    logger = logging.getLogger("sLogger")

    logger.info("Crawling started.")
    crawler = Crawler()
    crawler.crawl()
    logger.info("Crawling finished.")

    logger.info("Generating CSV files...")
    generate_data.generate()
    logger.info("CSV Files are generated.")

    sys.exit()


if __name__ == '__main__':
    main()
