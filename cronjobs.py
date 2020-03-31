from executes import run_agg_daily_app_store_data
from executes import run_analytics_user_base_daily

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

@sched.scheduled_job('cron',day_of_week='mon-sun',hour=2, id='daily_user_base')
def execute_analytics_user_base_daily():
    run_analytics_user_base_daily.cronjob()

sched.start()