# -*- coding: utf-8 -*-
from pathlib import Path
from funboost.constant import BrokerEnum, ConcurrentModeEnum
from funboost.helpers import FunctionResultStatusPersistanceConfig
from funboost.utils.simple_data_class import DataClassBase
from scheduler.common.hook import func_result

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$  以下是中间件连接配置    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
MONGO_CONNECT_URL = f'mongodb://127.0.0.1:27017'  # 如果有密码连接 'mongodb://myUserAdmin:8mwTdy1klnSYepNo@192.168.199.202:27016/admin'

RABBITMQ_USER = 'rabbitmq_user'
RABBITMQ_PASS = 'rabbitmq_pass'
RABBITMQ_HOST = '127.0.0.1'
RABBITMQ_PORT = 5672
RABBITMQ_VIRTUAL_HOST = '/'  # my_host # 这个是rabbitmq的虚拟子host用户自己创建的，如果你想直接用rabbitmq的根host而不是使用虚拟子host，这里写 / 即可。

REDIS_HOST = '127.0.0.1'
REDIS_PASSWORD = ''
REDIS_PORT = 6379
REDIS_DB = 8  # redis消息队列所在db，请不要在这个db放太多其他键值对，框架里面有的功能会scan扫描键名
REDIS_DB_FILTER_AND_RPC_RESULT = 8  # 如果函数做任务参数过滤 或者使用rpc获取结果，使用这个db，因为这个db的键值对多，和redis消息队列db分开

# 如果broker_kind 使用 peewee 中间件模式会使用mysql配置
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_DATABASE = 'testdb6'
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 以上是中间件连接配置    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# nb_log包的第几个日志模板，内置了7个模板，可以在你当前项目根目录下的nb_log_config.py文件扩展模板。
NB_LOG_FORMATER_INDEX_FOR_CONSUMER_AND_PUBLISHER = 12  # 7是简短的不可跳转，5是可点击跳转的，11是可显示ip 进程 线程的模板。

TIMEZONE = 'Asia/Shanghai'

# *********************************************** 以下是 boost装饰器的默认全局配置 *******************************************

class BoostDecoratorDefaultParams(DataClassBase):
    concurrent_mode = ConcurrentModeEnum.THREADING
    concurrent_num = 5
    qps: float = 0
    is_using_distributed_frequency_control = False
    is_send_consumer_hearbeat_to_redis = True
    consumin_function_decorator = None
    function_timeout = 3600*72     # 超时秒数，函数运行超过这个时间，则自动杀死函数执行的子线程
    max_retry_times = 0         # 0任务不重试
    log_level = 10
    logger_prefix = ''
    msg_expire_senconds = 0     # 任务过期，秒。因函数内部无法感知该事件，不建设使用该功能，业务内自行实现。
    task_filtering_expire_seconds = 0
    is_do_not_run_by_specify_time_effect = False    # 是否使不运行的时间段生效
    do_not_run_by_specify_time = ('10:00:00', '22:00:00')
    broker_kind: int = BrokerEnum.REDIS_STREAM
    user_custom_record_process_info_func = func_result
    function_result_status_persistance_conf = FunctionResultStatusPersistanceConfig(True, True,
                                                                                    1 * 24 * 3600, True)  # 配置。是否保存函数的入参，运行结果和运行状态到mongodb。
