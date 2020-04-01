import sys
sys.path.append('..')

import config

from datetime import datetime
import mysql.connector

def run_pipeline(table_name, pipeline_id=None):

    if not pipeline_id:
        pipeline_id = table_name

    print('{}: Starting job {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), pipeline_id))

    conn = mysql.connector.connect(
        user=config.DB_KLUP_USER,
        password=config.DB_KLUP_PASSWORD,
        host=config.DB_KLUP_HOST,
        database=config.DB_KLUP_NAME
    )

    with open('sql/{}/{}.ddl'.format(table_name, table_name), 'r') as file:
        ddl = file.read().format(db_name=config.DB_KLUP_NAME, table_name=table_name)

    with open('sql/{}/{}.sql'.format(table_name, table_name), 'r') as file:
        sql = file.read().format(db_name=config.DB_KLUP_NAME, table_name=table_name)

    cur = conn.cursor()
    cur.execute(ddl)
    cur.execute(sql)

    conn.commit()

    cur.close()
    conn.close()

    print('{}: Ending job {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), pipeline_id))


