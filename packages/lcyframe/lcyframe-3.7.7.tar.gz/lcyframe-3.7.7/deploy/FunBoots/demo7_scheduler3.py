from funboost.timing_job.apscheduler_use_redis_store import funboost_background_scheduler_redis_store
from funboost.timing_job.push_fun_for_apscheduler_use_db import push_for_apscheduler_use_db


"""
演示修改定时任务配置，从而影响到test_aps_redis_store脚本的定时任务变更(演示了定时间隔变化和入参变化)。

注意此脚本是关闭触发定时任务 apscheduler.start(paused=True)，因为此脚本是只负责修改 添加定时任务。不然此脚本和上面的脚本都执行定时任务那就不是我们想要的目的了。

下面这个一般就是在web服务接口中调用增删改查定时任务。我这里就不演示web接口了。web中只负责修改添加定时任务，让执行定时发布消息的任务在上面的test_aps_redis_store.py 脚本中和funboost消费一起启动
此文件是测试修改定时任务配置，另一个脚本的一启动的定时任务配置，会自动发生变化。因为定时任务配置通过中间件存储和通知了。
"""

# 在add_job前/后执行都可以
funboost_background_scheduler_redis_store.start(paused=True)  # 这个要设置为 paused=True，这个脚本是为了修改定时任务配置，这个要设置为 paused=True，这个脚本的sheduler不要运行，但一定要启动


# 第一种方式修改任务配置，使用 apscheduler.modify_job方法，但是_create_trigger方法有点冷门。

# funboost_background_scheduler_redis_store.modify_job(job_id='6',
#                                   trigger=funboost_background_scheduler_redis_store._create_trigger(
#                     trigger="interval",  # 指定新的执行任务方式，这里还是用的时间间隔
#                     trigger_args={"seconds": 2,}  # 多少分钟执行一次
#                 ),kwargs={"x": 2, "y": 3})



# 第二种方式修改任务配置，使用 apscheduler.add_job方法，对某个已存在的定时任务id修改，需要设置replace_existing=True
# funboost_background_scheduler_redis_store.add_job(push_for_apscheduler_use_db,   # 这里也可以用my_push函数，那样就不用传递函数文件和名字了，看demo7_scheduler2.py。
#                                                   'interval', id='6', name='namexx', seconds=3,
#                                                   args=('test_frame/test_apschedual/test_aps_redis_store.py', 'consume_func'), kwargs={"x": 20, "y": 30},
#                                                   replace_existing=True)

# 第三种方式修改任务配置
from demo7_scheduler2 import my_push
funboost_background_scheduler_redis_store.add_job(my_push,
                                                  'interval', id='6', name='namexx', seconds=3,
                                                  kwargs={"x": 20, "y": 30},
                                                  replace_existing=True)
