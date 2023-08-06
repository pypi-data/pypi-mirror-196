import apscheduler.jobstores.base
import datetime, time
from funboost import boost, BrokerEnum
from funboost.timing_job.apscheduler_use_redis_store import funboost_background_scheduler_redis_store
from funboost.timing_job.push_fun_for_apscheduler_use_db import push_for_apscheduler_use_db

'''
demo7_scheduler2.py和demo7_scheduler3.py  搭配测试，动态修改定时任务
demo7_scheduler3.py 中修改定时任务间隔和函数入参，demo7_scheduler2.py定时任务就会自动更新变化。
'''

@boost('queue_test_aps_redis', broker_kind=BrokerEnum.LOCAL_PYTHON_QUEUE)
def consume_func(x, y):
    print(f'{x} + {y} = {x + y}')


def my_push(x,y): # 推荐这样做，自己写个发布函数
    """
    可序列化
    设置了jobstores作业存储后，add_job调用的任务函数必须可序列化
    lambda、push、装饰器都不可以序列化
    """
    consume_func.push(x,y)

def serialize_agent(func, *func_args, **func_kwargs):
    """
    可序列化代理器
    与指定任务文件相对路径的方法原理一致
    func：add_job时指指定的任务对象
    func_args：任务的位置参数
    func_kwargs：任务的关键字参数

    设置了jobstores作业存储后，add_job调用的任务函数必须可序列化
    lambda、push、装饰器都不可以序列化

    添加任务：args第一个参数为任务函数
    from funboost.timing_job.apscheduler_use_redis_store import funboost_background_scheduler_redis_store
    sc = funboost_background_scheduler_redis_store
    sc.add_job(serialize_agent, 'interval', seconds=5, args=(demo.consume_func, 1, 2), id="1", name="name", replace_existing=True, jobstore="redis")
    或，其中kwargs["func"]为任务函数
    sc.add_job(serialize_agent, 'interval', seconds=5, kwargs={"func": demo.consume_func, "x": 10, "y": 20}, id="1", name="name", replace_existing=True, jobstore="redis")
    sc.add_job(serialize_agent, 'interval', seconds=30, kwargs={"func": "consume_func", "x": 2, "y": 3}, id="1", name="name", replace_existing=True)

    该方法有一个缺点是，func参数会被序列化到jobstore中，反序列化时需要本地环境上下文与序列化是一致，在分布式下可能存在问题
    该方法和官方推荐的通过指定文件路径原理一样，最后都是通过动态import任务对象进来直行.
    add_job(push_for_apscheduler_use_db, 'interval', seconds=5, args=('test_frame/test_apschedual/test_aps_redis_store.py', 'consume_func'), kwargs={"x": 5, "y": 6})
    def push_for_apscheduler_use_db:
        # 动态导入
        task_fun_file_for_import = task_fun_file.replace('/', '.').replace('.py', '')
        task_fun = getattr(importlib.import_module(task_fun_file_for_import), task_fun_name)
        task_fun.push(*args, **kwargs)

    最终写入ap.job的值，序列化前：
    {'version': 1, 'id': 'wam_id1', 'func': 'funboost.timing_job.push_fun_for_apscheduler_use_db:push_for_apscheduler_use_db', 'trigger': <IntervalTrigger (interval=datetime.timedelta(seconds=10), start_date='2022-12-26 20:23:28 CST', timezone='Asia/Shanghai')>, 'executor': 'default', 'args': ('funboost_events.wam', 'engine_wam_request'), 'kwargs': {'url': 'www.abc.com'}, 'name': 'wam_id1', 'misfire_grace_time': 300, 'coalesce': True, 'max_instances': 3, 'next_run_time': datetime.datetime(2022, 12, 26, 20, 24, 18, 523415, tzinfo=<DstTzInfo 'Asia/Shanghai' CST+8:00:00 STD>)}
    """

    return getattr(func, "push")(*func_args, **func_kwargs)
    # 或
    # from events import event_model
    # return getattr(event_model, func).push(*func_args, **func_kwargs)    # 也可以写成func.__name__


if __name__ == '__main__':
    consume_func.clear()

    # 需要这个类或者在add_job时指定任务的jobstore="redis"
    funboost_background_scheduler_redis_store.start(paused=False)

    try:
        # 不可序列化到job_store
        # funboost_background_scheduler_redis_store.add_job(consume_func.push,       # 使用数据库持久化定时任务，这样做是不行的，consume_func.push不可picke序列化存储到redis或者mysql mongo。
        #                                                   'interval', id='66', name='namexx', seconds=3,
        #                                                   kwargs={"x": 5, "y": 6},
        #                                                   replace_existing=False)

        # 可实现序列化到job_store
        # funboost_background_scheduler_redis_store.add_job(push_for_apscheduler_use_db, # 这个可以定时调用push_for_apscheduler_use_db，需要把文件路径和函数名字传来。
        #                                                   'interval', id='6', name='namexx', seconds=3,
        #                                                   args=('test_frame/test_apschedual/test_aps_redis_store.py', 'consume_func'), kwargs={"x": 5, "y": 6},
        #                                                   replace_existing=False)

        # 可实现序列化到job_store
        funboost_background_scheduler_redis_store.add_job(my_push,       # 这样做是可以的，用户自己定义一个函数，可picke序列化存储到redis或者mysql mongo。推荐这样。
                                                          'interval', id='6', name='namexx', seconds=15,
                                                          kwargs={"x": 5, "y": 6},
                                                          replace_existing=False)

        # TODO 删除数据库中所有已配置的定时任务，否则即使这里任务，已经存在于apscheduler.jobs的任务也会定时跑
        # funboost_background_scheduler_redis_store.remove_all_jobs()

    except apscheduler.jobstores.base.ConflictingIdError as e:
        print('定时任务id已存在： {e}')

    consume_func.consume()
    while True: time.sleep(10)

