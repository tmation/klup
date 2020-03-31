import config

import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
    user=config.DB_KLUP_USER,
    password=config.DB_KLUP_PASSWORD,
    host=config.DB_KLUP_HOST,
    database=config.DB_KLUP_NAME,
)

with open('sql/analytics_user_base_daily/analytics_user_base_daily.ddl','r') as file:
    ddl = file.read()

with open('sql/analytics_user_base_daily/analytics_user_base_daily.sql','r') as file:
    sql = file.read()

cur = conn.cursor()
cur.execute(ddl)
df = pd.DataFrame(cur.fetchall())
df.columns = cur.column_names

conn.close()