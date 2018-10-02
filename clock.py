import subprocess
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=10)
def timed_job():
    print('This job is run every 10 minutes.')
    subprocess.call("scrapy crawl -o items.jl items")
    subprocess.call("python write_rss.py")
    subprocess.call("python clean_rss.py")
    subprocess.call("python upload_rss.py")


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

sched.start()
