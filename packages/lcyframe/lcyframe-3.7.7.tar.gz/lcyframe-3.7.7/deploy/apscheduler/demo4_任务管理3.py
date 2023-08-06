import sys, time
import datetime

"""
任务操作
需要指定 job_stores 为redis/mysql(sqlachemy)/mongo 作为持久化，才能动态增删改查定时任务配置

"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

jobstores = {
    'redis': RedisJobStore(0)
}
# 执行器
executors = {
    'default': ThreadPoolExecutor(20),  # 默认，可以在job中单独指定
    # 'default': {'type': 'threadpool', 'max_workers': 20},
    # 建议尽量使用ProcessPoolExecutor进程池执行器，由于GIL的原因应避免使用线程池
    'processpool': ProcessPoolExecutor(5)   # 可以在job中单独指定processpool执行器
}
job_defaults = {
    'coalesce': True,      # 由于某个原因导致某个任务积攒了很多次没有执行（比如有一个任务是1分钟跑一次，但是系统原因断了5分钟），如果 coalesce=True，那么下次恢复运行的时候，会只执行一次，而如果设置 coalesce=False，那么就不会合并，会5次全部执行。
    'max_instances': 3,     # 同一个任务同一时间最多只能有5个实例在运行。比如一个耗时10分钟的job，被指定每分钟运行1次，如果我 max_instance值5，那么在第6~10分钟上，新的运行实例不会被执行，因为已经有5个实例在跑了。
    'misfire_grace_time': 600 # 错过了10分钟的任务不在执行
}
scheduler = BackgroundScheduler(
    jobstores=jobstores,
    executors=executors,
    job_defaults=job_defaults
)     # 需要非阻塞启动器
# from demo4_任务管理 import scheduler

scheduler.start(paused=True)          # 要设置为 paused=True，这个脚本是为了修改定时任务配置，不需要运行，但一定要启动

# 修改任务：覆盖，需要配置切job里指定相同的jobstores
# from demo1_job import test_tick2
# scheduler.add_job(test_tick2, 'interval', seconds=1, args=(20, 30), id="0002",
#                   replace_existing=True,
#                   jobstore="redis")
#
# # 删除任务：该job也将从其关联的job存储中删除，并且将不再执行。
# 有两种方法可以实现此目的：
# # 注意： 如果任务已经调度完毕，并且之后也不会再被执行的情况下，会被自动删除。
# scheduler.remove_job(job_id,jobstore=None)
# job.remove()
#
# # 暂停任务：
# job.pause()
# scheduler.pause_job("0002", jobstore="redis")
#
# time.sleep(5)
# # 恢复任务：
# job.resume()
print(scheduler.resume_job("0002", jobstore="redis"))

# 修改某个任务属性信息：除了id不能改，其他的属性都可以改
# changes={
#   'next_run_time': None,      # 等同于暂停任务.datetime.datetime(2022, 12, 20, 17, 11, 58, 82912, tzinfo=<DstTzInfo 'Asia/Shanghai' CST+8:00:00 STD>)
#   'trigger': <IntervalTrigger (interval=datetime.timedelta(seconds=5), start_date='2022-12-20 17:11:43 CST', timezone='Asia/Shanghai')>,
#   'executor': 'default',
#   'args': (2, 3),
#   'kwargs': {},
#   'name': 'test_tick1',
#   'misfire_grace_time': 600,
#   'coalesce': True,
#   'max_instances': 3,
# }
# scheduler.modify_job("0002", jobstore="redis",
#                      **{
#                          # 30秒后再运行
#                          "next_run_time": datetime.datetime.now() + datetime.timedelta(seconds=30)
#                      })

# 重新调度任务：
# scheduler.reschedule_job("job_id",jobstore=None,trigger=None,**trigger_args)
# scheduler.reschedule_job("0002", jobstore="redis", trigger='interval', seconds=1)

# 覆盖旧的方式修改作业
# scheduler.add_job("func", 'interval', seconds=5, id="0001", name="job1", replace_existing=True, kwargs={"x": 5, "y": 6})

# 输出作业信息：
# scheduler.print_jobs(jobstore=None, out=sys.stdout)
scheduler.print_jobs()
# 获取 job 列表:使用 get_jobs() 方法获取一个列表，或者使用 print_jobs() 方法打印一个格式化的列表。
# jobs = scheduler.get_jobs()	# 第二个参数可以指定任务储存器名称，那么就会获得对应任务储存器的任务列表。

# 可以使用 get_job(id) 获取单个 job 信息
# job_detail = scheduler.get_job("add_job_id")

# 用非阻塞的scheduler启动时，为了避免主进程退出，需要加
# while True: time.sleep(10)