from datetime import timedelta
from datetime import date

today = date.today()
#today = date(year = 2021 , month = 1, day = 11)

day_1 = today - timedelta(1)
start_day = date(year=2020, month = 12, day = 29)
day_1_yearmonth = day_1.strftime('%Y%m')