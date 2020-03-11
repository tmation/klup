import sys
sys.path.append('/db_statements')

import func_util_app_data as fu
import config
from db_statements.ddl import ddl_agg_daily_app_data
from db_statements.sql import sql_agg_daily_app_data

# Make DB Connection
conn = fu.make_db_connection(config)

# Get current month
# monthstr = '202001'
month_list = ['201901','201902','201903','201904','201905','201906','201907','201908','201909','201910','201911','201912']

for monthstr in month_list:
    # Get google report
    google_report = fu.get_google_installs_report(monthstr)
    google_report = fu.add_store_to_df(google_report, 'google')

    # Get apple report
    # PLACEHOLDER 1
    # PLACEHOLDER 2

    # Table DDL
    fu.create_table(ddl=ddl_agg_daily_app_data.ddl_table, con=conn)

    # Replace data
    fu.replace_operation(google_report, sql_agg_daily_app_data.insert_table, conn)

# Close connection
conn.close()
