from crawler.crawler import Crawler
import sys
import logging
import logging.config


def main():

    logging.config.fileConfig("logging.conf")
    logger = logging.getLogger("sLogger")
    logger.info("Crawling started.")

    crawler = Crawler()
    crawler.crawl()
    logger.info("Crawling finished.")

    sys.exit()


if __name__ == '__main__':
    main()
