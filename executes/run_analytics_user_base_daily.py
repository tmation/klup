import sys
sys.path.append('..')

import config

import mysql.connector

def cronjob():

    print('Starting job {}'.format('daily_analytics_user_base'))

    conn = mysql.connector.connect(
        user=config.DB_KLUP_USER,
        password=config.DB_KLUP_PASSWORD,
        host=config.DB_KLUP_HOST,
        database=config.DB_KLUP_NAME
    )

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

    print('Ending job {}'.format('daily_analytics_user_base'))


