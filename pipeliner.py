import sys
sys.path.append('..')

import config

from datetime import datetime
import mysql.connector

def run_pipeline(table_name, db_name=None, pipeline_id=None, query_params={}):

    if not pipeline_id:
        pipeline_id = table_name

    print('{}: Starting job {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), pipeline_id))
    if query_params:
        print('Query Parameters: {}'.format(query_params))

    conn = mysql.connector.connect(
        user=config.DB_KLUP_USER,
        password=config.DB_KLUP_PASSWORD,
        host=config.DB_KLUP_HOST,
        database=config.DB_KLUP_NAME
    )

    if db_name:
        db = db_name
    else:
        db = config.DB_KLUP_NAME

    with open('sql/{}/{}.ddl'.format(table_name, table_name), 'r') as file:
        ddl = file.read().format(db_name=db, table_name=table_name)

    with open('sql/{}/{}.sql'.format(table_name, table_name), 'r') as file:
        sql = file.read().format(db_name=db, table_name=table_name, **query_params)

    cur = conn.cursor()
    cur.execute(ddl)
    cur.execute(sql)

    conn.commit()

    cur.close()
    conn.close()

    print('{}: Ending job {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), pipeline_id))


