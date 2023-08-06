# 定时运行消费演示，定时方式入参用法可以百度 apscheduler 定时包。
import datetime, time
from funboost import boost, BrokerEnum, fsdf_background_scheduler, timing_publish_deco

@boost('queue_test_666', broker_kind=BrokerEnum.LOCAL_PYTHON_QUEUE)
def consume_func(x, y):
    print(f'{x} + {y} = {x + y}')


if __name__ == '__main__':
    fsdf_background_scheduler.add_job(timing_publish_deco(consume_func), 'interval', id='3_second_job', seconds=3,
                                      kwargs={"x": 5, "y": 6})  # 每隔3秒发布一次任务，自然就能每隔3秒消费一次任务了。
    # fsdf_background_scheduler.add_job(timing_publish_deco(consume_func), 'date',
    #                                   run_date=datetime.datetime(2020, 7, 24, 13, 53, 6), args=(5, 6,))  # 定时，只执行一次
    # fsdf_background_scheduler.add_timing_publish_job(consume_func, 'cron', day_of_week='*', hour=14, minute=51,
    #                                                  second=20, args=(5, 6,))  # 定时，每天的11点32分20秒都执行一次。

    # 启动定时
    fsdf_background_scheduler.start()
    # 启动消费,可以再其他地方启动消费进程
    # consume_func.consume()
    while True: time.sleep(10)  # 防止主进程退出，因为程序默认是schedule_tasks_on_main_thread = False，为了方便连续启动多个消费者消费， 没有在主线程调度运行，自己在代码结尾加个不让主线程结束的代码就行了。