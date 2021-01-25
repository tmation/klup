import sys

sys.path.append('..')

import func_util as fu
import constants as const

from sql.dashboard_refresh import QUERY


def cronjob(report):
	print('Starting job {}'.format(const.DASH_JOB_CONFIGS[report]['table_name']))

	sql = QUERY.format(table_name=const.DASH_JOB_CONFIGS[report]['table_name'],
	                   start_date=const.DASH_JOB_CONFIGS[report]['start_date'])
	fu.replace_worksheet_with_query(sql=sql, gsheet_id=const.KLUP_DASH_GSHEET_ID,
	                                worksheet_name=const.DASH_JOB_CONFIGS[report]['worksheet_name'])

	print('Ending job {}'.format(const.DASH_JOB_CONFIGS[report]['table_name']))


# cronjob('daily')
# cronjob('weekly')
# cronjob('monthly')

# report = 'monthly'
# sql = QUERY.format(table_name=const.DASH_JOB_CONFIGS[report]['table_name'],
# 	                   start_date=const.DASH_JOB_CONFIGS[report]['start_date'])