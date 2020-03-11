import sys
sys.path.append('/db_statements')

import func_util_app_data as fu
import config
from db_statements.ddl import ddl_agg_daily_app_data
from db_statements.sql import sql_agg_daily_app_data

from datetime import datetime

# Make DB Connection
conn = fu.make_db_connection(config)

# Get current month
monthstr = datetime.now().strftime('%Y%m')

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
