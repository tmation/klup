KLUP_DASH_GSHEET_ID = '1LidkympMzfpmy5UV1yWpqu6T63WvsLyWCTTEWV4qnb0'

DASH_JOB_CONFIGS = {
	'daily': {
		'table_name': 'agg_core_kpis_daily',
		'worksheet_name': 'data_daily',
		'start_date': '2020-01-01'
	},
	'weekly': {
		'table_name': 'agg_core_kpis_weekly',
		'worksheet_name': 'data_weekly',
		'start_date': '2020-01-01'
	},
	'monthly': {
		'table_name': 'agg_core_kpis_monthly',
		'worksheet_name': 'data_monthly',
		'start_date': '2017-07-01'
	},
	'testing': {
		'table_name': 'agg_core_kpis_monthly',
		'worksheet_name': 'TESTSHEET',
		'start_date': '2020-01-01'
	}
}
