import config

import mysql.connector
import pandas as pd
import pygsheets

import apiclient
import oauth2client

from google.cloud import storage

from google.oauth2 import service_account

from oauth2client.service_account import ServiceAccountCredentials

from google.cloud import storage

# Explicitly use service account credentials by specifying the private key
# file.
storage_client = storage.Client.from_service_account_json(
    config.GOOGLE_SERVICE_FILE)

# Make an authenticated API request
buckets = list(storage_client.list_buckets())
print(buckets)



credentials = service_account.Credentials.from_service_account_file(
    config.GOOGLE_SERVICE_FILE,
    scopes=[
        "https://www.googleapis.com/auth/devstorage.read_only",
    ],
)

from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/devstorage.read_only']
SERVICE_ACCOUNT_FILE = config.GOOGLE_SERVICE_FILE

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    # SERVICE_ACCOUNT_EMAIL,
    KEY_FILE,
    scopes=['https://www.googleapis.com/auth/devstorage.read_only']
)


credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

storage_client = storage.Client(credentials=credentials)

import googleapiclient.discovery

sqladmin = googleapiclient.discovery.build('devstorage', 'v1beta3', credentials=credentials)

storage_client = storage.Client.from_service_account_json()

bucket = storage_client.create_bucket('maxbucket')

print("Bucket {} created.".format(bucket.name))

buckets = list(storage_client.list_buckets())
print(buckets)

storage_client = storage.Client(credentials=credentials)

storage_client = storage.Client()

stored_credentials = apiclient.

pyg = pygsheets.authorize(client_secret='_secrets/klup_google_secret.json')














pyg = pygsheets.authorize(client_secret=config.GOOGLE_SECRET_FILE)

gsheet = pyg.open_by_key('1Y-OGMHowJHCqo7diT-AfpF7rhO1ZO2IVMfuH6-uWs0M')
print(gsheet.title)

cnx = mysql.connector.connect(
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    host=config.DB_HOST,
    database=config.DB_NAME
)

try:
   cursor = cnx.cursor()
   cursor.execute("""
      select distinct * from klup_staging.activity limit 10
   """)
   result = pd.DataFrame(cursor.fetchall())
   print(result)
finally:
    cnx.close()