import sys

sys.path.append('..')
sys.path.append('/submodules')
sys.path.append('/sql')

import config
# from appfigures_py import appfigures_py

from submodules.appfigures_py import appfigures_py

from datetime import datetime, timedelta
import mysql.connector

af = appfigures_py.AppFigures(
    config.AF_CLIENT_ID,
    config.AF_CLIENT_SECRET,
    config.AF_ACCESS_TOKEN,
    config.AF_ACCESS_TOKEN_SECRET,
)

conn = mysql.connector.connect(
    user=config.DB_KLUP_USER,
    password=config.DB_KLUP_PASSWORD,
    host=config.DB_KLUP_HOST,
    database=config.DB_KLUP_NAME
)

def convert_keys_to_string(dictionary):
    """Recursively converts dictionary keys to strings."""
    if not isinstance(dictionary, dict):
        return dictionary
    return dict((str(k), convert_keys_to_string(v))
        for k, v in dictionary.items())

def get_store_reports_per_day(start_date):
    end_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
    report = af.get_downloads(start_date, end_date)

    store_report_list = []
    for store in report.keys():
        store_report = report[store]
        store_report.update({'day': start_date})

        for k, v in store_report.items():
            try:
                if isinstance(v, unicode):
                    store_report[k] = float(v)
            except:
                try:
                    store_report[k] = str(v)
                except:
                    pass

        store_report_list.append(store_report)

    return store_report_list

def replace_data(sql, data, conn):
    data = convert_keys_to_string(data)
    cursor = conn.cursor()
    cursor.execute(sql, data)
    conn.commit()


