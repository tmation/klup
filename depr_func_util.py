import sys
sys.path.append('/submodules')
sys.path.append('/submodules/appfollow_api')

import config
import constants as const

from submodules.gcloud_storage_py import gcloud_storage_py
from appfollow_api import api
from appfollow_api import api

cid = '72551'
api_secret = '2EnHfxXe7kChmAgmWkVw'

data = api.collections()


gcs = gcloud_storage_py.GCloudStorage(config.GOOGLE_SERVICE_FILE)

def get_google_installs_report(month):
    '''Returns a DF for metrics specified in config for all days available in a given month.'''
    # month = month sting in format 202001

    df = gcs.get_blop_as_df(
        bucket_name=config.G_STORAGE_BUCKET_NAME,
        source_blob_name='stats/installs/installs_com.xxxxtech.klup_' + month + '_overview.csv',
        destination_file_name='installs' + month + '.csv',
        delete_file=True
    )

    print(df.columns)
    print(const.COLUMNS_INSTALL_REPORT_ORIGINAL)

    df = df[const.COLUMNS_INSTALL_REPORT_ORIGINAL]
    df.columns = const.COLUMS_INSTALL_REPORT_FINAL

    return df

