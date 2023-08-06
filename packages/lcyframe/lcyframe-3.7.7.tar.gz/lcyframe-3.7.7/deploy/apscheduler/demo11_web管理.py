import sys
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import logging
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

"""
管理界面
https://blog.csdn.net/mx472756841/article/details/114319306

"""
