from datetime import datetime


def parse_date(date):
    date_object = datetime.strptime(date, "%b %d, %Y")
    return date_object


str_date = "Jun 2, 1987"
dt_date = parse_date(str_date)
print(dt_date)


