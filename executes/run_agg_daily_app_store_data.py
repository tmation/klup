from archive import config
import func_util as fu
from sql import agg_daily_app_store_data

import datetime
import mysql.connector

from apscheduler.schedulers.blocking import BlockingScheduler

def cronjob_update_app_daily_app_store_data():

    conn = mysql.connector.connect(
        user=config.DB_KLUP_USER,
        password=config.DB_KLUP_PASSWORD,
        host=config.DB_KLUP_HOST,
        database=config.DB_KLUP_NAME
    )

    # start = datetime.datetime.strptime("2020-01-01", "%Y-%m-%d")
    # end = datetime.datetime.strptime("2020-03-10", "%Y-%m-%d")

    start = (datetime.datetime.now() - datetime.timedelta(days=2))
    end = (datetime.datetime.now() - datetime.timedelta(days=0))
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

    date_list = []
    for date in date_generated:
        date_list.append(date.strftime("%Y-%m-%d"))

    for date in date_list:
        data_stores = fu.get_store_reports_per_day(date)
        data = fu.convert_keys_to_string(data_stores[0])

        for data in data_stores:
            print(data)
            fu.replace_data(agg_daily_app_store_data.replace, data, conn)

    conn.close()

sched = BlockingScheduler()

@sched.scheduled_job('cron',day_of_week='mon-sun',hour=3)
def scheduled_job():
    cronjob_update_app_daily_app_store_data()

sched.start()