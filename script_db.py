import config
import mysql.connector

import pandas as pd

conn = mysql.connector.connect(
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    host=config.DB_HOST,
    database=config.DB_NAME
)

