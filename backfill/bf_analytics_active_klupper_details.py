import sys
sys.path.append('..')

from pipeliner import run_pipeline

run_pipeline(table_name='analytics_active_klupper_details', db_name='klup_production')


