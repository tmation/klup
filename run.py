import config
import func_util as fu
from sql import agg_daily_app_store_data

import datetime
import mysql.connector


conn = mysql.connector.connect(
    user=config.DB_KLUP_USER,
    password=config.DB_KLUP_PASSWORD,
    host=config.DB_KLUP_HOST,
    database=config.DB_KLUP_NAME
)

# SELECT TEST
# cursor = conn.cursor()
# cursor.execute('SELECT MAX(day) FROM klup_tmation.agg_daily_app_store_data')
# print(cursor.fetchall())

# API DATA TEST
# start = datetime.datetime.strptime("2019-01-01", "%Y-%m-%d")
# end = datetime.datetime.strptime("2019-01-02", "%Y-%m-%d")
# date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
#
# date_list = []
# for date in date_generated:
#     date_list.append(date.strftime("%Y-%m-%d"))
#
# for date in date_list:
#     data_stores = fu.get_store_reports_per_day(date)
#     # data = fu.convert_keys_to_string(data_stores[0])
#
#     for data in data_stores:
#         print(data)
#         fu.replace_data(agg_daily_app_store_data.replace, data, conn)

# MODELLING TEST
with open('sql/analytics_user_base_daily/analytics_user_base_daily.ddl', 'r') as file:
    ddl = file.read()

with open('sql/analytics_user_base_daily/analytics_user_base_daily.sql', 'r') as file:
    sql = file.read()

cur = conn.cursor()

cur.execute(ddl)
cur.execute(sql)

conn.commit()

cur.close()
conn.close()

