# 定时运行消费演示，定时方式入参用法可以百度 apscheduler 定时包。
import datetime, time
from funboost import boost, BrokerEnum, fsdf_background_scheduler, timing_publish_deco
from apscheduler.triggers.cron import CronTrigger
class MyCronTrigger(CronTrigger):
    @classmethod
    def my_from_crontab(cls, expr, timezone=None):
        values = expr.split()
        if len(values) == 7:
            return cls(second=values[0], minute=values[1], hour=values[2], day=values[3], month=values[4],
                       day_of_week=values[5], year=values[6], timezone=timezone)
        elif len(values) == 5:
            return CronTrigger.from_crontab(expr)
        else:
            raise ValueError('cron表达式错误，支持格式：[分时日月周]、[秒分时日月周年]')


@boost('queue_test_666', broker_kind=BrokerEnum.LOCAL_PYTHON_QUEUE)
def consume_func(x, y):
    print(f'{x} + {y} = {x + y}')


if __name__ == '__main__':
    fsdf_background_scheduler.add_job(consume_func, trigger=MyCronTrigger.my_from_crontab("*/1 * * * *"), id="0002", name="job2", args=(7, 8))
    fsdf_background_scheduler.add_job(consume_func, trigger=MyCronTrigger.my_from_crontab("*/1 * * * * * *"), id="0003", name="job3", args=(9, 10))

    # 启动定时
    fsdf_background_scheduler.start()
    # 启动消费,可以再其他地方启动消费进程
    # consume_func.consume()
    while True: time.sleep(10)  # 防止主进程退出，因为程序默认是schedule_tasks_on_main_thread = False，为了方便连续启动多个消费者消费， 没有在主线程调度运行，自己在代码结尾加个不让主线程结束的代码就行了。