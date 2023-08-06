import sys
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import logging
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

"""
日志调试
如果 APScheduler 工作不正常，可以开启日志 DEBUG 模式

"""

scheduler = BlockingScheduler()  # 阻塞，同一时间只有一个定时任务被执行
scheduler._logger = logging
scheduler.start()