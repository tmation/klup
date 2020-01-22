import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='klupmariadb.mariadb.database.azure.com',
                             user='tmation_staging@klupmariadb',
                             password='lb3SKHtrlumQ',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor
                             )
