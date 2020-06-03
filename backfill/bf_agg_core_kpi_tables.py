import sys
sys.path.append('..')

from pipeliner import run_pipeline

import datetime
from tqdm import tqdm

# start = (datetime.datetime.now() - datetime.timedelta(days=111))
# end = (datetime.datetime.now() - datetime.timedelta(days=0))
#
# date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
#
# date_list = []
# for date in date_generated:
#     date_list.append(date.strftime("%Y-%m-%d"))
#
# for date in tqdm(date_list):
# 	run_pipeline(table_name='agg_core_kpis_daily', db_name='klup_production',query_params={'START_DATE':'2020-04-01','END_DATE':'2020-04-02','TIME_INTERVAL':'DAY'})

# run_pipeline(table_name='agg_core_kpis_daily', db_name='klup_production',query_params={'START_DATE':'2017-07-01','END_DATE':'2017-12-31','TIME_INTERVAL':'DAY'})
# run_pipeline(table_name='agg_core_kpis_daily', db_name='klup_production',query_params={'START_DATE':'2018-01-01','END_DATE':'2018-12-31','TIME_INTERVAL':'DAY'})
# run_pipeline(table_name='agg_core_kpis_daily', db_name='klup_production',query_params={'START_DATE':'2019-01-01','END_DATE':'2019-12-31','TIME_INTERVAL':'DAY'})
# run_pipeline(table_name='agg_core_kpis_daily', db_name='klup_production',query_params={'START_DATE':'2020-01-01','END_DATE':'2020-05-01','TIME_INTERVAL':'DAY'})
run_pipeline(table_name='agg_core_kpis_daily', db_name='klup_production',query_params={'START_DATE':'2020-05-01','END_DATE':'2020-05-07','TIME_INTERVAL':'DAY'})

run_pipeline(table_name='agg_core_kpis_weekly', db_name='klup_production',query_params={'START_DATE':'2017-07-01','END_DATE':'2017-12-31','TIME_INTERVAL':'WEEK'})
run_pipeline(table_name='agg_core_kpis_weekly', db_name='klup_production',query_params={'START_DATE':'2018-01-01','END_DATE':'2018-12-31','TIME_INTERVAL':'WEEK'})
run_pipeline(table_name='agg_core_kpis_weekly', db_name='klup_production',query_params={'START_DATE':'2019-01-01','END_DATE':'2019-12-31','TIME_INTERVAL':'WEEK'})
run_pipeline(table_name='agg_core_kpis_weekly', db_name='klup_production',query_params={'START_DATE':'2020-04-01','END_DATE':'2020-06-01','TIME_INTERVAL':'WEEK'})

run_pipeline(table_name='agg_core_kpis_monthly', db_name='klup_production',query_params={'START_DATE':'2017-07-01','END_DATE':'2017-12-31','TIME_INTERVAL':'MONTH'})
run_pipeline(table_name='agg_core_kpis_monthly', db_name='klup_production',query_params={'START_DATE':'2018-01-01','END_DATE':'2018-12-31','TIME_INTERVAL':'MONTH'})
run_pipeline(table_name='agg_core_kpis_monthly', db_name='klup_production',query_params={'START_DATE':'2019-01-01','END_DATE':'2019-12-31','TIME_INTERVAL':'MONTH'})
run_pipeline(table_name='agg_core_kpis_monthly', db_name='klup_production',query_params={'START_DATE':'2020-01-01','END_DATE':'2020-05-01','TIME_INTERVAL':'MONTH'})


