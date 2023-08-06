from datetime import datetime
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

"""
定时任务框架：APScheduler
创建新的CronTrigger类MyCronTrigger，支持到cron秒
"""
# 精确到分
print(CronTrigger.from_crontab("*/5 * * * *"))

# 精确到秒
from apscheduler.triggers.cron import CronTrigger


# 重写Cron定时
class MyCronTrigger(CronTrigger):
    # def __init__(self, year=None, month=None, day=None, week=None, day_of_week=None, hour=None,
    #              minute=None, second=None, start_date=None, end_date=None, timezone=None,
    #              jitter=None):
    #     super().__init__(year=None, month=None, day=None, week=None, day_of_week=None, hour=None,
    #              minute=None, second=None, start_date=None, end_date=None, timezone=None,
    #              jitter=None)
    @classmethod
    def my_from_crontab(cls, expr, timezone=None):
        values = expr.split()
        if len(values) != 7:
            raise ValueError('Wrong number of fields; got {}, expected 7'.format(len(values)))

        return cls(second=values[0], minute=values[1], hour=values[2], day=values[3], month=values[4],
                   day_of_week=values[5], year=values[6], timezone=timezone)


def test_tick1(x, y):
    print(x, y)
    print('1 The time is: %s' % datetime.now())

def test_tick2(x, y):
    print(x, y)
    print('2 The time is: %s' % datetime.now())

def test_tick3(x, y):
    print(x, y)
    print("crontab指定时间运行")


if __name__ == '__main__':
    """
    各类调度器适用场景如下：
    1、BlockingScheduler：适用于调度程序是进程中唯一运行的进程，调用start函数会阻塞当前线程，不能立即返回
    2、BackgroundScheduler：适用于调度程序在应用程序的后台运行，调用start后主线程不会阻塞
    3、AsyncIOScheduler：适用于使用了asyncio模块的应用程序
    4、GeventScheduler：适用于使用gevent模块的应用程序
    5、TwistedScheduler：适用于构建Twisted的应用程序
    6、QtScheduler：适用于构建Qt的应用程序
    """
    from pytz import utc
    from apscheduler.schedulers.background import BackgroundScheduler
    from funboost import funboost_config_deafult as funboost_config
    from apscheduler.jobstores.redis import RedisJobStore
    from apscheduler.jobstores.memory import MemoryJobStore
    from apscheduler.jobstores.mongodb import MongoDBJobStore
    from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
    from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

    # 作业存储
    # MemoryJobStore：没有序列化，任务存储在内存中，增删改查都是在内存中完成。
    # SQLAlchemyJobStore：使用 SQLAlchemy这个 ORM框架作为存储方式。
    # MongoDBJobStore：使用 mongodb作为存储器。
    # RedisJobStore：使用 redis作为存储器。
    jobstores = {
        # 'mongo': MongoDBJobStore(),
        # # 'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
        # 'default': MemoryJobStore
        "default": RedisJobStore(funboost_config.REDIS_DB,
                               host=funboost_config.REDIS_HOST,
                               port=funboost_config.REDIS_PORT,
                               password=funboost_config.REDIS_PASSWORD
                           )        # redis = RedisJobStore().redis
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
        'coalesce': False,      # 由于某个原因导致某个任务积攒了很多次没有执行（比如有一个任务是1分钟跑一次，但是系统原因断了5分钟），如果 coalesce=True，那么下次恢复运行的时候，会只执行一次，而如果设置 coalesce=False，那么就不会合并，会5次全部执行。
        'max_instances': 3,     # 同一个任务同一时间最多只能有5个实例在运行。比如一个耗时10分钟的job，被指定每分钟运行1次，如果我 max_instance值5，那么在第6~10分钟上，新的运行实例不会被执行，因为已经有5个实例在跑了。
        'misfire_grace_time': 600 # 错过了10分钟的任务不在执行
    }

    scheduler = BlockingScheduler(
        jobstores=jobstores,
        executors=executors,
        job_defaults=job_defaults,
        # timezone=utc
    )
    # scheduler = BackgroundScheduler()     # 非阻塞

    # 固定间隔执行
    # scheduler.add_job(test_tick1, 'interval', seconds=5, id="0001", name="job1", kwargs={"x": 5, "y": 6})

    # crontab定时任务：只精确到分
    # scheduler.add_job(test_tick2, 'cron', hour="18-19", minute='*/1', id="0002", name="job2", kwargs={"x": 7, "y": 8})
    # # 指定cron表达式
    # scheduler.add_job(test_tick2, CronTrigger.from_crontab("*/1 * * * *"), id="0002", name="job2", args=(7, 8))
    # # 在6月，7月，8月，11月和12月的第三个星期五的00:00,01:00,02:00和03:00执行test_tick2
    # scheduler.add_job(test_tick2, 'cron', month='6-8,11-12', day='3rd fri', hour='0-3', id="0002", name="job2",
    #               kwargs={"x": 7, "y": 8})
    # # 在2014-05-30 00:00:00之前，从周一到周五每天5:30 (am) 运行。
    # scheduler.add_job(test_tick2, 'cron', day_of_week='mon-fri', hour=5, minute=30, end_date='2014-05-30')
    # TODO 重写crontab类，精确到秒
    scheduler.add_job(test_tick2, MyCronTrigger.my_from_crontab("10,20,30 * * * * * *"), id="0002", name="job2", args=(7, 8))

    # date日期任务，一次性的
    from datetime import date
    # scheduler.add_job(test_tick3, 'date', run_date=date(2022, 12, 12),  id="0002", name="job2", args=[9, 10])
    # 10秒后执行，一次性的
    # scheduler.add_job(test_tick3, 'date', run_date=datetime.datetime.now()+datetime.timedelta(seconds=10),  id="0002", name="job2", args=[9, 10])

    # # 批量运行1000个
    # for i in range(1000):
    #     import random
    #
    #     scheduler.add_job(test_tick1, 'interval', seconds=random.randint(5, 60), id=str(i), name="job1",
    #                       kwargs={"x": 5, "y": 6})

    # jitter选项使您可以将随机添加到执行时间。如果您有多个服务器并且不希望它们在同一时刻运行作业，或者您希望阻止作业在繁忙时段运行，那么这可能很有用：
    # 运行 `test_tick3` 在[-120，+120]秒中随机选择一个额外延迟时间,避免重叠
    # scheduler.add_job(test_tick3, 'cron', hour='*', jitter=120)

    # job指定执行器
    scheduler.add_job(
        test_tick2,
        MyCronTrigger.my_from_crontab("10,20,30 * * * * * *"),
        id="0002",
        name="job2",
        args=(7, 8),
        jobstore="jobstore_name",   # 默认default
        executor="processpool"      # 默认default，需提前在BackgroundScheduler()中需要配置了executor
    )

    # 获取redis客户端
    redis = scheduler._jobstores["default"].redis

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

