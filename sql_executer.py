import config

import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
        user=config.DB_KLUP_USER,
        password=config.DB_KLUP_PASSWORD,
        host=config.DB_KLUP_HOST,
        database=config.DB_KLUP_NAME
)

sql_file = 'sql/agg_core_kpis_daily/agg_core_kpis_daily.sql'

with open(sql_file, 'r') as f:
	sql = f.read().format(START_DATE='2020-03-20',END_DATE='2020-03-21')

cur = conn.cursor()
cur.execute(sql)

resp = cur.fetchall()

results = pd.DataFrame(resp)
results.columns = cur.column_names