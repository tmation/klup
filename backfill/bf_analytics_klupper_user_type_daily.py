import sys
sys.path.append('..')

from pipeliner import run_pipeline

import datetime
from tqdm import tqdm

# start = (datetime.datetime.now() - datetime.timedelta(days=111))
# end = (datetime.datetime.now() - datetime.timedelta(days=0))
# date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

sdate = datetime.date(2020, 1, 1)
edate = datetime.date(2020, 5, 1)
delta = edate - sdate

date_generated = []
for i in range(delta.days + 1):
    day = sdate + datetime.timedelta(days=i)
    date_generated.append(day)

date_list = []
for date in date_generated:
    date_list.append(date.strftime("%Y-%m-%d"))

for date in tqdm(date_list):
	run_pipeline(table_name='analytics_klupper_user_type_daily', db_name='klup_production',query_params={'DATE':date})


