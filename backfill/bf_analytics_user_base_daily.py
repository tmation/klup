import sys
sys.path.append('..')

from pipeliner import run_pipeline

run_pipeline(table_name='analytics_user_base_daily', db_name='klup_production')


