import sys
sys.path.append('/submodules')
sys.path.append('/ddl')
sys.path.append('/sql')

import config
import constants as const
from ddl.agg_daily_app_data import ddl_table
from sql.agg_daily_app_data import insert_table

from submodules.gcloud_storage_py import gcloud_storage_py

import pandas as pd
pd.options.display.max_columns = 10
import pygsheets

import mysql.connector

gcs = gcloud_storage_py.GCloudStorage(config.GOOGLE_KLUP_SERVICE_FILE)
# pyg = pygsheets.authorize(service_account_file=config.GOOGLE_TMATION_SERVICE_FILE)
conn = mysql.connector.connect(
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    host=config.DB_HOST,
    database=config.DB_NAME
)

def get_google_installs_report(month):
    '''Returns a DF for metrics specified in config for all days available in a given month.'''
    # month = month sting in format 202001

    df = gcs.get_blop_as_df(
        bucket_name=config.G_STORAGE_BUCKET_NAME,
        source_blob_name='stats/installs/installs_com.xxxxtech.klup_' + month + '_overview.csv',
        destination_file_name='installs' + month + '.csv',
        delete_file=True
    )

    df = df[const.COLUMNS_INSTALL_REPORT_ORIGINAL]
    df.columns = const.COLUMS_INSTALL_REPORT_FINAL

    return df

def add_store_to_df(df, store):
    df['store'] = store
    return df

def create_table(ddl):
    cursor = conn.cursor()
    cursor.execute(ddl)
    cursor.close()

def replace_operation(df, sql):
    for row in range(df.shape[0]):
        data = {
            'day':str(df.loc[row, 'day']),
            'store':str(df.loc[row, 'store']),
            'user_installs':int(df.loc[row, 'user_installs']),
            'user_uninstalls':int(df.loc[row, 'user_uninstalls']),
            'total_user_installs':int(df.loc[row, 'total_user_installs']),
            'device_installs':int(df.loc[row, 'device_installs']),
            'device_uninstalls':int(df.loc[row, 'device_uninstalls']),
            'active_device_installs':int(df.loc[row, 'active_device_installs']),
            'install_events':int(df.loc[row, 'install_events']),
            'update_events':int(df.loc[row, 'update_events']),
            'uninstall_events':int(df.loc[row, 'uninstall_events']),
        }
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
        cursor.close()

rep = get_google_installs_report('202003')
create_table(ddl_table)
rep = add_store_to_df(rep, 'google')

replace_operation(rep, insert_table)

conn.close()



