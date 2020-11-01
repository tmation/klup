from executes import run_agg_daily_app_store_data
from executes import run_dashboard_refresh

from pipeliner import run_pipeline

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from datetime import datetime, timedelta, date

today = datetime.now().strftime('%Y-%m-%d')
today_minus_3_day = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
today_minus_7_day = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
day_first_last_month = (datetime.today().replace(day=1, month=datetime.today().month - 1)).strftime('%Y-%m-%d')

if date.today().weekday() == 0:
    this_monday = today
else:
    this_monday = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime('%Y-%m-%d')

last_monday = (datetime.now() - timedelta(days=datetime.now().weekday()) - timedelta(days=7)).strftime('%Y-%m-%d')
last_2x_monday = (datetime.now() - timedelta(days=datetime.now().weekday()) - timedelta(days=14)).strftime('%Y-%m-%d')




sched = BlockingScheduler()


def my_listener(event):
    if event.exception:
        print('The job crashed :(')
    else:
        print('The job worked :)')


sched.add_listener(my_listener, EVENT_JOB_ERROR)


# AGG_DAILY_APP_STORE_DATA
@sched.scheduled_job('cron', day_of_week='mon-sun', hour=16, id='daily_app_store_data')
def execute_agg_daily_app_store_data():
    run_agg_daily_app_store_data.cronjob()


# ANALYTICS_ACTIVE_KLUPPER_DETAILS
@sched.scheduled_job('cron', day_of_week='mon-sun', hour=2, id='analytics_active_klupper_details')
def execute_analytics_active_klupper_details():
    run_pipeline(db_name='klup_production', table_name='analytics_active_klupper_details')


# ANALYTICS_USER_BASE_DAILY
@sched.scheduled_job('cron', day_of_week='mon-sun', hour=2, id='analytics_user_base_daily')
def execute_analytics_user_base_daily():
    run_pipeline(db_name='klup_production', table_name='analytics_user_base_daily')


# ANALYTICS_FRIENDSHIPS_DAILY
@sched.scheduled_job('cron', day_of_week='mon-sun', hour=2, id='analytics_friendships_daily')
def execute_analytics_friendships_daily():
    run_pipeline(db_name='klup_production', table_name='analytics_friendships_daily', query_params={'DATE': today})


# ANALYTICS_KLUPPER_USER_TYPE_DAILY
@sched.scheduled_job('cron', day_of_week='mon-sun', hour=2, id='analytics_klupper_user_type_daily')
def execute_analytics_klupper_user_type_daily():
    run_pipeline(db_name='klup_production', table_name='analytics_klupper_user_type_daily',
                 query_params={'DATE': today})


# AGG_CORE_KPIS_DAILY
@sched.scheduled_job('cron', day_of_week='mon-sun', hour=5, id='agg_core_kpis_daily')
def execute_agg_core_kpis_daily():
    run_pipeline(db_name='klup_production', table_name='agg_core_kpis_daily',
                 query_params={'START_DATE': today_minus_7_day, 'END_DATE': today, 'TIME_INTERVAL': 'DAY'})


# AGG_CORE_KPIS_WEEKLY
@sched.scheduled_job('cron', day_of_week='mon', hour=5, id='agg_core_kpis_weekly')
def execute_agg_core_kpis_weekly():
    run_pipeline(db_name='klup_production', table_name='agg_core_kpis_weekly',
                 query_params={'START_DATE': last_2x_monday, 'END_DATE': this_monday, 'TIME_INTERVAL': 'WEEK'})


# AGG_CORE_KPIS_MONTHLY
@sched.scheduled_job('cron', day='1', hour=5, id='agg_core_kpis_monthly')
def execute_agg_core_kpis_monthly():
    run_pipeline(db_name='klup_production', table_name='agg_core_kpis_monthly',
                 query_params={'START_DATE': day_first_last_month, 'END_DATE': today, 'TIME_INTERVAL': 'MONTH'})


### GSHEET JOBS
# DATA_DAILY
@sched.scheduled_job('cron', day_of_week='mon-sun', hour=6, minute=0, id='data_daily')
def execute_data_daily():
    run_dashboard_refresh.cronjob('daily')


# DATA_WEEKLY
@sched.scheduled_job('cron', day_of_week='mon', hour=6, minute=10, id='data_weekly')
def execute_data_weekly():
    run_dashboard_refresh.cronjob('weekly')


# DATA_MONTHLY
@sched.scheduled_job('cron', day='1', hour=6, minute=20, id='data_monthly')
def execute_data_monthly():
    run_dashboard_refresh.cronjob('monthly')


sched.start()
