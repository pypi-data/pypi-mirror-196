from datetime import datetime
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.base import STATE_STOPPED, STATE_PAUSED, STATE_RUNNING

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
    from funboost import funboost_config_deafult as funboost_config
    from apscheduler.jobstores.redis import RedisJobStore
    from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

    jobstores = {
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
    # TODO 重写crontab类，精确到秒
    scheduler.add_job(test_tick2, MyCronTrigger.my_from_crontab("10,20,30 * * * * * *"), id="0002", name="job2", args=(7, 8))

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
    # 或
    # from funboost.utils import decorators, time_util, RedisMixin
    # redis = RedisMixin().redis_db_frame

    try:
        scheduler.start()
        print("==========调度引擎启动成功==========")
        while bool(redis.blpop("engine_update_event") or True):  # 是否存在引擎更新事件
            event_name = redis.get("apscheduler_execute_active")  # 操作指令 pause暂停调度；resume/start恢复调度
            try:
                if event_name == b"pause" and scheduler.state is STATE_RUNNING:
                    print("检测到消费者（引擎）需要更新，调度已暂停")
                    scheduler.pause()
                elif event_name == b"resume" and scheduler.state is STATE_PAUSED:
                    print("检测到消费者（引擎）需要完毕，调度已恢复")
                    scheduler.resume()
                elif scheduler.state is STATE_STOPPED:
                    print("调度服务已退出【shutdown()】，SchedulerNotRunningError")
                else:
                    print("检测到【engine_update_event】事件，获取到操作指令[apscheduler_execute_active]: %s" % event_name or "None")
            except Exception as e:
                print("检测到调度服务异常，已关闭；【e错误信息】: %s" % str(e))
                scheduler.shutdown()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

