import sys
sys.path.append('..')

import config
import func_util as fu
from pipeliner import run_pipeline

from sql import agg_daily_app_store_data

import datetime
import mysql.connector

conn = mysql.connector.connect(
        user=config.DB_KLUP_USER,
        password=config.DB_KLUP_PASSWORD,
        host=config.DB_KLUP_HOST,
        database=config.DB_KLUP_NAME
    )

# ANALYTICS TABLES
# run_pipeline(table_name='analytics_user_base_daily')
# run_pipeline(table_name='analytics_friendships_daily')
# run_pipeline(table_name='analytics_active_klupper_details')

# APP STORE DATA
start = (datetime.datetime.now() - datetime.timedelta(days=20))
end = (datetime.datetime.now() - datetime.timedelta(days=0))
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days)]

print('Start Date: '.format(start.strftime('%Y-%m-%d')))
print('End Date: '.format(end.strftime('%Y-%m-%d')))

date_list = []
for date in date_generated:
    date_list.append(date.strftime("%Y-%m-%d"))

# date_list = ['2020-04-03','2020-04-04']

for date in date_list:
    data_stores = fu.get_store_reports_per_day(date)

    for data in data_stores:
        data['_loaded_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(date)
        print(data)
        print('\n')
        fu.replace_data(agg_daily_app_store_data.replace, data, conn)

conn.close()

print('Ending job {}'.format('daily_app_store_data'))

# KPI TABLES
run_pipeline(table_name='agg_core_kpis_daily',query_params={'START_DATE':'2020-04-07','END_DATE':'2020-04-08','TIME_INTERVAL':'DAY'})
run_pipeline(table_name='agg_core_kpis_weekly',query_params={'START_DATE':'2020-01-01','END_DATE':'2020-04-06','TIME_INTERVAL':'WEEK'})
run_pipeline(table_name='agg_core_kpis_monthly',query_params={'START_DATE':'2020-01-01','END_DATE':'2020-04-06','TIME_INTERVAL':'MONTH'})