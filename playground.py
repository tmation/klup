import config

import mysql.connector
import pandas as pd
import pygsheets


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
   result = cursor.fetchall()
   print(result)
finally:
    cnx.close()