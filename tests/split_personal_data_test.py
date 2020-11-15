from crawler.crawler_utils import CrawlerUtils

personal_data = "36y.o. (Jun 29, 1984) 186cm 86kg"

g = CrawlerUtils.split_personal_data(personal_data)

print(g)
