import sys
sys.path.append('..')

from pipeliner import run_pipeline

import datetime
from tqdm import tqdm

start = (datetime.datetime.now() - datetime.timedelta(days=111))
end = (datetime.datetime.now() - datetime.timedelta(days=0))

date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

date_list = []
for date in date_generated:
    date_list.append(date.strftime("%Y-%m-%d"))

for date in tqdm(date_list):
	run_pipeline(table_name='analytics_friendships_daily', db_name='klup_production',query_params={'DATE':date})


