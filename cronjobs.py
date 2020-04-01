from executes import run_agg_daily_app_store_data

from pipeliner import import run_pipeline

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

sched = BlockingScheduler()

def my_listener(event):
    if event.exception:
        print('The job crashed :(')
    else:
        print('The job worked :)')

sched.add_listener(my_listener, EVENT_JOB_ERROR)

@sched.scheduled_job('cron',day_of_week='mon-sun',hour=6,id='daily_app_store_data')
def execute_agg_daily_app_store_data():
    run_agg_daily_app_store_data.cronjob()

# ANALYTICS_USER_BASE_DAILY
@sched.scheduled_job('cron',day_of_week='mon-sun',hour=2, id='analytics_user_base_daily')
def execute_analytics_user_base_daily():
    run_pipeline('analytics_user_base_daily')

# ANALYTICS_FRIENDSHIPS_DAILY
@sched.scheduled_job('cron',day_of_week='mon-sun',hour=2, id='analytics_friendships_daily')
def execute_analytics_friendships_daily():
    run_pipeline('analytics_friendships_daily')

# ANALYTICS_ACTIVE_KLUPPER_DETAILS
@sched.scheduled_job('cron',day_of_week='mon-sun',hour=2, id='analytics_active_klupper_details')
def execute_analytics_active_klupper_details():
    run_pipeline('analytics_active_klupper_details')

sched.start()