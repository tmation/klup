from pipeliner import run_pipeline

import pandas as pd
import time

start_date = '2020-02-01'
end_date = '2020-03-31'

dates = pd.date_range(start_date, end_date). tolist()

for date in dates:
	print('Start {}'.format(date.strftime('%Y-%m-%d')))
	run_pipeline('analytics_klupper_user_type_daily', query_params={'DATE': date.strftime('%Y-%m-%d')})
	time.sleep(5)
	print('End {}'.format(date.strftime('%Y-%m-%d')))

run_pipeline('analytics_klupper_user_type_daily', query_params={'DATE': '2020-03-01'})

