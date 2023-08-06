import sys
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

"""
调度器监听事件
add_listen
https://www.cnblogs.com/leffss/p/11912364.html
"""

def my_listener(event):
    """
    调度器事件只有在某些情况下才会被触发，并且可以携带某些有用的信息。
    通过 add_listener() 传递适当参数，可以实现监听不同是事件，比如 job 运行成功、运行失败等。具体支持的事件类型见官方文档
    """
    if event.exception:
        print('The job crashed :(')
    else:
        print('The job worked :)')

scheduler = BlockingScheduler()  # 阻塞，同一时间只有一个定时任务被执行
scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)