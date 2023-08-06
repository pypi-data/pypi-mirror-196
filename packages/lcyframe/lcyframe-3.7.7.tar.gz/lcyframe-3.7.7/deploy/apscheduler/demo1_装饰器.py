from datetime import datetime
import os, time
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

"""
定时任务框架：APScheduler
"""
from apscheduler.scheduler import Scheduler

sched = Scheduler()

@sched.interval_schedule(seconds=2,misfire_grace_time=3600)
def excute_task():
    fun()  #执行任务函数

sched.start()  #启动定时任务脚本
# ————————————————
# 版权声明：本文为CSDN博主「名难取aaa」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/m0_69082030/article/details/126939574