import sys
sys.path.append('..')

import config
import func_util as fu
from sql import agg_daily_app_store_data

import datetime
import mysql.connector
# from tqdm import tqdm

print('Starting job {}'.format('daily_app_store_data'))

conn = mysql.connector.connect(
    user=config.DB_KLUP_USER,
    password=config.DB_KLUP_PASSWORD,
    host=config.DB_KLUP_HOST,
    database=config.DB_KLUP_NAME
)

start = (datetime.datetime.now() - datetime.timedelta(days=1000))
end = (datetime.datetime.now() - datetime.timedelta(days=0))
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

sdate = datetime.date(2020, 5, 5)
edate = datetime.date(2020, 8, 21)
delta = edate - sdate

date_generated = []
for i in range(delta.days + 1):
    day = sdate + datetime.timedelta(days=i)
    date_generated.append(day)

print('Start Date: {}'.format(min(date_generated).strftime('%Y-%m-%d')))
print('End Date: {}'.format(max(date_generated).strftime('%Y-%m-%d')))

date_list = []
for date in date_generated:
    date_list.append(date.strftime("%Y-%m-%d"))

for date in date_list:
    data_stores = fu.get_store_reports_per_day(date)

    for data in data_stores:
        data['_loaded_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        fu.replace_data(agg_daily_app_store_data.replace, data, conn)

conn.close()

print('Ending job {}'.format('daily_app_store_data'))


