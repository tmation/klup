import config
import httplib2
from oauth2client.service_account import ServiceAccountCredentials
from apiclient import discovery
from google.cloud import storage

SERVICE_ACCOUNT_EMAIL = 'tmation@klup-1533128107823.iam.gserviceaccount.com'
KEY_FILE = config.GOOGLE_SERVICE_FILE

import json

with open(config.GOOGLE_SERVICE_FILE) as f:
    data = json.loads(f.read())
    x = dict(data)

# Create an httplib2.Http object to handle our HTTP requests and to
# authorize them correctly.
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    # SERVICE_ACCOUNT_EMAIL,
    KEY_FILE,
    scopes=['https://www.googleapis.com/auth/devstorage.read_only']
)

http = httplib2.Http()
http = credentials.authorize(http)

# Read the first page of features in a Table.
service = discovery.build('storage', 'v1', http=http)

bucketName = 'pubsite_prod_rev_12827242350245133610'
report = 'reviews/reviews_com.xxxxtech.klup_201912.csv'

test = service.objects().get(bucket=bucketName,object=report).execute()

##################################################

storage_client = storage.Client.from_service_account_json(
    config.GOOGLE_SERVICE_FILE)

destination_file_name = 'test.csv'

bucket = storage_client.get_bucket(bucketName)

bucket = storage_client.get_bucket(bucket_name)
# Create a blob object from the filepath
blob = bucket.blob("stats/installs/installs_nl.kluppen.android.klup_202001_overview.csv")
# Download the file to a destination
blob.download_to_filename(destination_file_name)


def list_files(bucketName):
    """List all files in GCP bucket."""
    files = bucket.list_blobs(prefix=bucketName)
    fileList = [file.name for file in files if '.' in file.name]
    return fileList

list_files(bucket)

storage_client = storage.Client()
bucket = storage_client.get_bucket(bucketName)