import configparser
import os

from kombu import Queue, Exchange, serialization
broker_url = "redis://:@localhost:6379/4"  # 使用 rabbitmq 作broker
result_backend = "redis://:@localhost:6379/4"
#
#
# try:
#     serialization.registry._decoders.pop("application/x-python-serialize")
# except:pass
#
# file_path = os.environ.get('PROJECT_ENV_FILE')
# cf = configparser.ConfigParser()
# cf.read(file_path)
#
# # broker_url = redis_backend_uri
# broker_url = rabbitmq_broker_uri        # 使用 rabbitmq 作broker
# result_backend = redis_backend_uri

# worker_concurrency = 10  # 并发worker数
# CELERYD_FORCE_EXECV = True  # 非常重要,有些情况下可以防止死锁
worker_max_tasks_per_child = 1  # 防止内存泄露
timezone = "Asia/Shanghai"
enable_utc = True
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['pickle', 'json']
task_ignore_result = True
task_time_limit = 3600*24

task_track_started = True
result_expires = 3600*24


# task_queues = (
#     Queue('default', exchange=Exchange('default', type='direct'), routing_key='default'),
#     Queue("module_search", exchange=Exchange("module_search", type='direct'), routing_key="module_search"),
#     Queue("task_search", exchange=Exchange("task_search", type='direct'), routing_key="task_search"),
#     Queue("process_url", exchange=Exchange("process_url", type='direct'), routing_key="process_url"),
#     Queue("start_go", exchange=Exchange("start_go", type='direct'), routing_key="start_go"),
# )
#
# task_routes = {
#     'module_monitor.tasks.*': {'queue': 'module_search', 'routing_key': 'module_search'},
#     'censor_main.tasks.process_url': {'queue': 'process_url', 'routing_key': 'process_url'},
#     'censor_main.tasks.start_go': {'queue': 'start_go', 'routing_key': 'start_go'},
#     'censor_main.tasks.render': {'queue': 'start_go', 'routing_key': 'start_go'},
#     'censor_main.tasks.*': {'queue': 'task_search', 'routing_key': 'task_search'},
#     'censor_wam.tasks.*': {'queue': 'task_search', 'routing_key': 'task_search'},
#     # '*': {'queue': 'default', 'routing_key': 'default'},
# }
