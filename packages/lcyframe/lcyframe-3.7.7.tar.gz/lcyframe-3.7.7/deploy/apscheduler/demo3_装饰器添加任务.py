from datetime import datetime
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

"""
装饰器使用
https://www.cjavapy.com/article/128/
"""
scheduler = BlockingScheduler()  # 阻塞，同一时间只有一个定时任务被执行

@scheduler.scheduled_job('interval', id='1', seconds=5, args=(1, 2))
def test_tick1(x, y):
    print(x, y)
    print('1 The time is: %s' % datetime.now())

@scheduler.scheduled_job('interval', id='2', day='last sun', args=(1, 2))
def test_tick2(x, y):
    print(x, y)
    print('2 The time is: %s' % datetime.now())

@scheduler.scheduled_job('cron', hour="18-19", minute='*/1', id="0003", name="job3", kwargs={"x": 9, "y": 10})
def test_tick3(x, y):
    print(x, y)
    print("crontab指定时间运行")


if __name__ == '__main__':
    scheduler.start()