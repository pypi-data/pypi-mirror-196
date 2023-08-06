from funboost.timing_job.apscheduler_use_redis_store import funboost_background_scheduler_redis_store
from funboost.timing_job.push_fun_for_apscheduler_use_db import push_for_apscheduler_use_db
import time
"""
此文件是测试修改定时任务配置，另一个脚本的一启动的定时任务配置，会自动发生变化。因为定时任务配置通过中间件存储和通知了。
"""



# 第一种方式修改任务配置，使用 apscheduler.modify_job方法，但是_create_trigger方法有点冷门。

# funboost_background_scheduler_redis_store.modify_job(job_id='6',
#                                   trigger=funboost_background_scheduler_redis_store._create_trigger(
#                     trigger="interval",  # 指定新的执行任务方式，这里还是用的时间间隔
#                     trigger_args={"seconds": 2,}  # 多少分钟执行一次
#                 ),kwargs={"x": 2, "y": 3})


funboost_background_scheduler_redis_store.start(paused=True)  # 这个要设置为 paused=True，这个脚本是为了修改定时任务配置，这个要设置为 paused=True，这个脚本的sheduler不要运行，但一定要启动
# TODO 切记，如果job_store采用持久化保存，删除任务时，确保队列里任务至少保留一个，不能清空，否则后续新添加进去的任务，无法被ap识别，如果一定需要清空任务，则必须在清空后马上新增一个任务进去，这是个巨坑BUG。
# funboost_background_scheduler_redis_store.remove_all_jobs()
funboost_background_scheduler_redis_store.remove_job("16")
time.sleep(3)
funboost_background_scheduler_redis_store.add_job(push_for_apscheduler_use_db,   # 这里也可以用 my_push函数秒，那样就不用传递函数的位置和名字了，看test_aps_redis_store.py。
          'interval', id='17', name='namexx17', seconds=5,
          args=('test_aps_redis_store.py', 'consume_func'), kwargs={"x": 17, "y": 4},
          replace_existing=True)
