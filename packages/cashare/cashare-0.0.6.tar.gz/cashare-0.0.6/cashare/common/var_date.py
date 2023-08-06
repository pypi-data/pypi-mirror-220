
import datetime
import pandas as pd
import dateutil.relativedelta
import time

def check_date(start_date,end_date):
    today = datetime.date.today().strftime('%Y-%m-%d')


    if start_date >today:
        return "start_date大于现在时间"
    elif start_date > end_date:
        return "start_date大于end_date"
    elif end_date > today:
        return end_date== today