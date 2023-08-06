from datetime import datetime
import os, time
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

"""
定时任务框架：APScheduler
"""

def test_tick1(x, y):
    """
    如果我们的执行器或任务储存器是会序列化任务的，那么任务就必须符合：
    1-回调函数必须全局可用；
    2-回调函数参数必须也是可以被序列化的
    内置任务储存器中，只有MemoryJobStore不会序列化任务；
    内置执行器中，只有ProcessPoolExecutor会序列化任务。

    序列化到redis的任务格式：pickle.loads(job_state)
        {
            'version': 1,
            'id': '0001',
            'func': 'demo1_job:test_tick1',
            'trigger': <IntervalTrigger (interval=datetime.timedelta(seconds=5), start_date='2022-12-20 17:11:43 CST', timezone='Asia/Shanghai')>,
            'executor': 'default',
            'args': (2, 3),
            'kwargs': {},
            'name':
            'test_tick1',
            'misfire_grace_time': 600,
            'coalesce': True,
            'max_instances': 3,
            'next_run_time': datetime.datetime(2022, 12, 20, 17, 11, 58, 82912, tzinfo=<DstTzInfo 'Asia/Shanghai' CST+8:00:00 STD>)
        }
    """
    with open("assa", "w") as f:
        f.write("sddsssd\n")
    print(x, y)
    print('1 The time is: %s' % datetime.now())

def test_tick2(x, y):
    print(x, y)
    print('2 The time is: %s' % datetime.now())

def test_tick3(x, y):
    print(x, y)
    print("crontab指定时间运行")


"""
各类调度器适用场景如下：
1、BlockingScheduler：适用于调度程序是进程中唯一运行的进程，调用start函数会阻塞当前线程，不能立即返回
2、BackgroundScheduler：适用于调度程序在应用程序的后台运行，调用start后主线程不会阻塞
3、AsyncIOScheduler：适用于使用了asyncio模块的应用程序
4、GeventScheduler：适用于使用gevent模块的应用程序
5、TwistedScheduler：适用于构建Twisted的应用程序
6、QtScheduler：适用于构建Qt的应用程序
"""
scheduler = BlockingScheduler()  # 阻塞，同一时间只有一个定时任务被执行
# scheduler = BackgroundScheduler()     # 非阻塞

if __name__ == '__main__':
    # 默认情况下，每个 job 仅允许 1 个实例同时运行。这意味着，如果该 job 将要运行，但是前一个实例尚未完成，则最新的 job 不会调度。可以在添加 job 时指定 max_instances 参数解除限制。
    # scheduler.add_job(test_tick1, 'interval', seconds=5, id="0001", name="job1", kwargs={"x": 5, "y": 6})
    # job = scheduler.add_job(test_tick2, 'interval', seconds=10, id="0002", name="job2", kwargs={"x": 7, "y": 8})
    # job.pause()  # 暂停
    # scheduler.pause_job('0001')    # 暂停

    # 如果想立即运行job ，则可以在添加 job 时省略 trigger 参数；
    # scheduler.add_job(test_tick2, id="0002", name="job2", kwargs={"x": 7, "y": 8})

    """
    添加 job 时的日期设置参数 start_date、end_date 以及 run_date都支持字符串格式
    1：'2019-12-31' 或者 '2019-12-31 12:01:30'
    2：datetime.date（datetime.date(2019, 12, 31)） 
    3：datetime.datetime（datetime.datetime(2019, 12, 31, 16, 30, 1)）；
    4：datetime.datetime.now()+datetime.timedelta(seconds=10),
    """

    try:
        scheduler.start()                 # 注意：调度器启动后就无法更改配置了。
        # scheduler.start(paused=True)    # paused = True以这种方式启动的调度器直接就是暂停状态。
        # scheduler.start(paused=True)

        # 用非阻塞的scheduler启动时，为了避免主进程退出，需要加
        # while True: time.sleep(10)
    except (KeyboardInterrupt, SystemExit):
        # 关闭调度器方法：
        scheduler.shutdown()
        # 默认情况下，会关闭 job 存储和执行器，并等待所有正在执行的 job 完成。如果不想等待则可以使用以下方法关闭：
        # scheduler.shutdown(wait=False)

        # if sc.state is STATE_RUNNING:
        #     print("检测到消费者（引擎）需要更新，调度已暂停")
        #     sc.pause()
        # elif sc.state is STATE_PAUSED:
        #     print("引擎升级完毕，调度已恢复")
        #     sc.resume()
        # elif sc.state is STATE_STOPPED:
        #     print("调度服务已退出【shutdown()】，SchedulerNotRunningError")
        # 暂停调度器：
        # scheduler.pause()
        # # 恢复调度器：
        # scheduler.resume()

        # TODO
        # import atexit               # 该模块可以实现，程序退出前进行一些操作，和信号捕获效果类似
        # atexit.register(lambda: x.shutdown(wait=False))   # 任然不会退出主进程