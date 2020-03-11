from executes import run_agg_daily_app_store_data

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('cron',day_of_week='mon-sun',hour=3)
def run_agg_daily_app_store_data():
    run_agg_daily_app_store_data.cronjob()

sched.start()