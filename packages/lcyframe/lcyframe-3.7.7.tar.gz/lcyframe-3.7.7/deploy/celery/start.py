from celery import Celery, platforms

# --------------- 信号处理 ---------------
from signals import sig         # 装载信号处理
from signals import revoked     # 装载信号处理

# root启动: 如有必要（不推荐）
platforms.C_FORCE_ROOT = True

app = Celery("deploy.celery.works.demo")

# 加载配置
app.config_from_object("config")

# 可见性超时会影响任务重新传递，时间低于 apply_async 的 countdown 时会导致任务多跑
# https://docs.celeryq.dev/en/latest/getting-started/backends-and-brokers/redis.html#visibility-timeout
# app.conf.broker_transport_options = {'visibility_timeout': 3600*24*30*366}

# worker status
# app.control.inspect()


# celery worker启动时自动发现有哪些任务函数
app.autodiscover_tasks([
    'works.demo',
    'works.tasks',
])

app.conf.beat_schedule = {
    "task_name": {
        "task": "works.demo.add",                           # 需要执行的任务
        "schedule": 13,                                     # 13秒轮询一次
        "args": (),
        'options': {'queue': 'task_search'},                # 将任务放进该队列
    }
}


"""
pycharm启动配置
scrip：/Users/apple/python/python3.9/bin/celery
params: -A start worker --autoscale=1,4 --loglevel=INFO
"""