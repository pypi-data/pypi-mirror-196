import os
import time
from pytz import utc
from sqlalchemy import func

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ProcessPoolExecutor

"""
任务操作
需要指定 job_stores 为redis/mysql(sqlachemy)/mongo 作为持久化，才能动态增删改查定时任务配置
"""
jobstores = {
    # 可以配置多个存储
    #'mongo': {'type': 'mongodb'},
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')  # SQLAlchemyJobStore指定存储链接
}
executors = {
    'default': {'type': 'threadpool', 'max_workers': 20},     # 最大工作线程数20
    'processpool': ProcessPoolExecutor(max_workers=5)         # 最大工作进程数为5
}
job_defaults = {
    'coalesce': False,   # 关闭新job的合并，当job延误或者异常原因未执行时
    'max_instances': 3   # 并发运行新job默认最大实例多少
}

scheduler = BackgroundScheduler()
scheduler.configure(jobstores=jobstores,
                    executors=executors,
                    job_defaults=job_defaults
                    # timezone=utc  # utc作为调度程序的时区
                    )

def print_time(name):
    print(f'{name} - {time.ctime()}')

def add_job(job_id, func, args, seconds):
    """添加job"""
    print(f"添加间隔执行任务job - {job_id}")
    scheduler.add_job(id=job_id, func=func, args=args, trigger='interval', seconds=seconds)

def add_coun_job(job_id, func, args, start_time):
    """添加job"""
    print(f"添加一次执行任务job - {job_id}")
    scheduler.add_job(id=job_id, func=func, args=args, trigger='date',timezone='Asia/Shanghai', run_date=start_time)
    # scheduler.add_job(func=print_time, trigger='date',timezone='Asia/Shanghai', run_date=datetime(2022, 2, 19, 17, 57, 0).astimezone(), args=['text2'])

def remove_job(job_id):
    """移除job"""
    scheduler.remove_job(job_id)
    print(f"移除job - {job_id}")

def pause_job(job_id):
    """停止job"""
    scheduler.pause_job(job_id)
    print(f"停止job - {job_id}")

def resume_job(job_id):
    """恢复job"""
    scheduler.resume_job(job_id)
    print(f"恢复job - {job_id}")

def get_jobs():
    """获取所有job信息,包括已停止的"""
    res = scheduler.get_jobs()
    print(f"所有job - {res}")

def print_jobs():
    print(f"详细job信息")
    scheduler.print_jobs()

def start():
    """启动调度器"""
    scheduler.start()

def shutdown():
    """关闭调度器"""
    scheduler.shutdown()

if __name__ == '__main__':
    start()

    print('Press Ctrl+{0} to exit \n'.format('Break' if os.name == 'nt' else 'C'))
    add_job('job_A', func=print_time, args=("A", ), seconds=1)
    # add_job('job_B', func=print_time, args=("B", ), seconds=2)
    # time.sleep(6)
    # pause_job('job_A') # 停止a
    # get_jobs()   #得到所有job
    # time.sleep(6)
    # print_jobs()
    # resume_job('job_A')
    # time.sleep(6)
    # remove_job('job_A')

    # 用非阻塞的scheduler启动时，为了避免主进程退出，需要加
    while True: time.sleep(10)
