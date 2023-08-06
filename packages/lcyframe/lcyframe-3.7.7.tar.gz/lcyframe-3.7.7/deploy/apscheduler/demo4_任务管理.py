import sys, time
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

# from demo1_job import scheduler
from demo1_job import test_tick1, test_tick2, test_tick3

"""任务操作：
需要指定 job_stores 为redis/mysql(sqlachemy)/mongo 作为持久化，才能动态增删改查定时任务配置
https://www.cnblogs.com/leffss/p/11912364.html
"""
from apscheduler.schedulers.background import BackgroundScheduler
# 作业存储
# MemoryJobStore：没有序列化，任务存储在内存中，增删改查都是在内存中完成。
# SQLAlchemyJobStore：使用 SQLAlchemy这个 ORM框架作为存储方式。
# MongoDBJobStore：使用 mongodb作为存储器。
# RedisJobStore：使用 redis作为存储器。
jobstores = {
    # 'mongo': MongoDBJobStore(),
    # 'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
    # 'default': MemoryJobStore
    'default': RedisJobStore(8)
}
# 执行器
executors = {
    'default': ThreadPoolExecutor(20),  # 默认，可以在job中单独指定
    # 'default': {'type': 'threadpool', 'max_workers': 20},
    # 建议尽量使用ProcessPoolExecutor进程池执行器，由于GIL的原因应避免使用线程池
    'processpool': ProcessPoolExecutor(5)   # 可以在job中单独指定processpool执行器
}
# 高级配置
"""
当由于某种原因导致某个 job 积攒了好几次没有实际运行（比如说系统挂了 5 分钟后恢复，有一个任务是每分钟跑一次的，
按道理说这 5 分钟内本来是“计划”运行 5 次的，但实际没有执行），如果 coalesce 为 True，下次这个 job 被 
submit 给 executor 时，只会执行 1 次，也就是最后这次，如果为 False，那么会执行 5 次（不一定，因为还有其他
条件，看后面misfire_grace_time）。misfire_grace_time：单位为秒，假设有这么一种情况,当某一 job 被调度时
刚好线程池都被占满，调度器会选择将该 job 排队不运行，misfire_grace_time 参数则是在线程池有可用线程时会比对
该 job 的应调度时间跟当前时间的差值，如果差值小于 misfire_grace_time 时，调度器会再次调度该 job；反之该 
job 的执行状态为 EVENTJOBMISSED 了，即错过运行。
coalesce 与 misfire_grace_time 可以在初始化调度器的时候设置一个全局默认值，添加任务时可以再单独指定
"""
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

if __name__ == '__main__':
    scheduler.start()

    # 添加任务：
    scheduler.add_job(test_tick2, 'interval', seconds=5, args=(2, 3), id="0002",
                      replace_existing=True,
                      # executor="processpool"
                      )
    # scheduler.remove_all_jobs()
    # TODO 切记，如果job_store采用持久化保存，删除任务时，确保队列里任务至少保留一个，不能清空，否则后续新添加进去的任务，无法被ap识别
    #  如果一定需要清空任务，则必须在清空后马上新增一个任务进去，这是个巨坑BUG。
    #  sc.remove_all_jobs()
    #  sc.add_job(default_task, 'interval', seconds=60, id="default_task")
    # # 删除任务：该job也将从其关联的job存储中删除，并且将不再执行。有两种方法可以实现此目的：
    # # 注意： 如果任务已经调度完毕，并且之后也不会再被执行的情况下，会被自动删除。
    # scheduler.remove_job(job_id,jobstore=None)
    # job.remove()
    #
    # # 暂停任务：
    # job.pause()
    # scheduler.pause_job(job_id,jobstore=None)
    #
    # # 恢复任务：
    # job.resume()
    # scheduler.resume_job(job_id,jobstore=None)

    # 修改某个任务属性信息：
    # scheduler.modify_job("0002", jobstore=None, **changes)

    # 修改单个作业的触发器并更新下次运行时间：
    # scheduler.reschedule_job(job_id,jobstore=None,trigger=None,**trigger_args)

    # 覆盖旧的方式修改作业
    # scheduler.add_job("func", 'interval', seconds=5, id="0001", name="job1", replace_existing=True, kwargs={"x": 5, "y": 6})

    # 输出作业信息：
    # scheduler.print_jobs(jobstore=None, out=sys.stdout)

    # 获取 job 列表:使用 get_jobs() 方法获取一个列表，或者使用 print_jobs() 方法打印一个格式化的列表。
    # jobs = scheduler.get_jobs()	# or
    # scheduler.print_jobs()
    # # 提示：可以使用 get_job(id) 获取单个 job 信息
    # job_detail = scheduler.get_job("add_job_id")

    # 用非阻塞的scheduler启动时，为了避免主进程退出，需要加
    while True: time.sleep(10)