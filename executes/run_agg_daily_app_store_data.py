import sys
sys.path.append('..')

import config
import func_util as fu
from sql import agg_daily_app_store_data

import datetime
import mysql.connector

def cronjob():

    conn = mysql.connector.connect(
        user=config.DB_KLUP_USER,
        password=config.DB_KLUP_PASSWORD,
        host=config.DB_KLUP_HOST,
        database=config.DB_KLUP_NAME
    )

    start = (datetime.datetime.now() - datetime.timedelta(days=2))
    end = (datetime.datetime.now() - datetime.timedelta(days=0))
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

    date_list = []
    for date in date_generated:
        date_list.append(date.strftime("%Y-%m-%d"))

    for date in date_list:
        data_stores = fu.get_store_reports_per_day(date)

        for data in data_stores:
            fu.replace_data(agg_daily_app_store_data.replace, data, conn)

    conn.close()


