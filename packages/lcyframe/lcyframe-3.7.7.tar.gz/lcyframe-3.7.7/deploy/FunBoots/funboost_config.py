# -*- coding: utf-8 -*-

from pathlib import Path
from funboost.constant import BrokerEnum, ConcurrentModeEnum
from funboost.helpers import FunctionResultStatusPersistanceConfig
from funboost.utils.simple_data_class import DataClassBase

'''
此文件是第一次运行框架自动生成刀项目根目录的，不需要用由户手动创建。
此文件里面可以写任意python代码。例如 中间件 帐号 密码自己完全可以从apola配置中心获取或者从环境变量获取。
'''

'''
你项目根目录下自动生成的 funboost_config.py 文件中修改配置，会被自动读取到。

此文件按需修改，例如你使用redis中间件作为消息队列，可以不用管rabbitmq mongodb kafka啥的配置。
但有3个功能例外，如果你需要使用rpc模式或者分布式控频或者任务过滤功能，无论设置使用何种消息队列中间件都需要把redis连接配置好，
如果@boost装饰器设置is_using_rpc_mode为True或者 is_using_distributed_frequency_control为True或do_task_filtering=True则需要把redis连接配置好，默认是False。


框架使用文档是 https://funboost.readthedocs.io/zh_CN/latest/

'''

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$  以下是中间件连接配置    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# 开启消费状态、结果web页面 https://funboost.readthedocs.io/zh/latest/articles/c4.html#web
MONGO_CONNECT_URL = f'mongodb://127.0.0.1:27017'  # 如果有密码连接 'mongodb://myUserAdmin:8mwTdy1klnSYepNo@192.168.199.202:27016/admin'

RABBITMQ_USER = 'rabbitmq_user'
RABBITMQ_PASS = 'rabbitmq_pass'
RABBITMQ_HOST = '127.0.0.1'
RABBITMQ_PORT = 5672
RABBITMQ_VIRTUAL_HOST = '/'  # my_host # 这个是rabbitmq的虚拟子host用户自己创建的，如果你想直接用rabbitmq的根host而不是使用虚拟子host，这里写 / 即可。

REDIS_HOST = '127.0.0.1'
REDIS_PASSWORD = ''
REDIS_PORT = 6379
REDIS_DB = 7  # redis消息队列所在db，请不要在这个db放太多其他键值对，框架里面有的功能会scan扫描键名
REDIS_DB_FILTER_AND_RPC_RESULT = 8  # 如果函数做任务参数过滤 或者使用rpc获取结果，使用这个db，因为这个db的键值对多，和redis消息队列db分开

NSQD_TCP_ADDRESSES = ['127.0.0.1:4150']
NSQD_HTTP_CLIENT_HOST = '127.0.0.1'
NSQD_HTTP_CLIENT_PORT = 4151

KAFKA_BOOTSTRAP_SERVERS = ['127.0.0.1:9092']

SQLACHEMY_ENGINE_URL = 'sqlite:////sqlachemy_queues/queues.db'

# 如果broker_kind 使用 peewee 中间件模式会使用mysql配置
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_DATABASE = 'testdb6'

# persist_quque中间件时候采用本机sqlite的方式，数据库文件生成的位置。如果linux账号在根目录没权限建文件夹，可以换文件夹。
SQLLITE_QUEUES_PATH = '/sqllite_queues'

TXT_FILE_PATH = Path(__file__).parent / 'txt_queues'  # 不建议使用这个txt模拟消息队列中间件，本地持久化优先选择 PERSIST_QUQUE 中间件。

ROCKETMQ_NAMESRV_ADDR = '192.168.199.202:9876'

MQTT_HOST = '127.0.0.1'
MQTT_TCP_PORT = 1883

HTTPSQS_HOST = '127.0.0.1'
HTTPSQS_PORT = '1218'
HTTPSQS_AUTH = '123456'

NATS_URL = 'nats://192.168.6.134:4222'

KOMBU_URL = 'redis://127.0.0.1:6379/0'
# KOMBU_URL =  'sqla+sqlite:////dssf_kombu_sqlite.sqlite'  # 4个//// 代表磁盘根目录下生成一个文件。推荐绝对路径。3个///是相对路径。
# https://funboost.readthedocs.io/zh/latest/articles/c6.html#redis-clusterredis
# KOMBU_URL = 'sentinel://root:redis@localhost:26079;sentinel://root:redis@localhost:26080;sentinel://root:redis@localhost:26081'

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ 以上是中间件连接配置    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# nb_log包的第几个日志模板，内置了7个模板，可以在你当前项目根目录下的nb_log_config.py文件扩展模板。
NB_LOG_FORMATER_INDEX_FOR_CONSUMER_AND_PUBLISHER = 11  # 7是简短的不可跳转，5是可点击跳转的，11是可显示ip 进程 线程的模板。
FSDF_DEVELOP_LOG_LEVEL = 50  # 作者开发时候的调试代码的日志，仅供我自己用，所以日志级别跳到最高，用户不需要管。

TIMEZONE = 'Asia/Shanghai'

# *********************************************** 以下是 boost装饰器的默认全局配置 *******************************************
"""
BoostDecoratorDefaultParams是@boost装饰器默认的全局入参。如果boost没有亲自指定某个入参，就自动使用这里的配置。
这里的值不用配置，在boost装饰器中可以为每个消费者指定不同的入参，除非你嫌弃每个 boost 装饰器相同入参太多了，那么可以设置这里的全局默认值。

例如用户不想每次在boost装饰器指定broker_kind为哪种消息队列，可以设置broker_kind为用户自己希望的默认消息队列类型

boost入参可以ide跳转到boost函数的docstring查看
boost入参也可以看文档3.3章节  https://funboost.readthedocs.io/zh/latest/articles/c3.html  

BoostDecoratorDefaultParams这个类的属性名字和boost装饰器的入参名字一模一样，只有 queue_name 必须每个装饰器是不同的名字，不能作为全局的。
所以boost装饰器只有一个是必传参数。
"""


class BoostDecoratorDefaultParams(DataClassBase):
    # 单个消费者内的并发模式
    # 1 多线程(ConcurrentModeEnum.THREADING)
    # 2 gevent(ConcurrentModeEnum.GEVENT)
    # 3 eventlet(ConcurrentModeEnum.EVENTLET)
    # 4 asyncio(ConcurrentModeEnum.ASYNC)
    # 5 单线程(ConcurrentModeEnum.SINGLE_THREAD)
    concurrent_mode = ConcurrentModeEnum.THREADING

    # 默认50，请设置1000以下，如果设置了qps，可忽略这个设置，框架自动计算需要开启多少个线程
    # 如果你启动了4个wokr(task.multi_process_consume(4)),则消费并发是：4*concurrent_num（和开发者确认过了）
    # 每一个消费者在启动瞬间，会从队列里面预取一部分任务放到内存里，如果任务较少的情况下，会导致后启动的消费者没有任务了，所以并发看上去可能不是4*concurrent_num
    # 随着队列里不断新增任务，每个消费者都会陆续取到任务进行消费，当任务足够多，就会达到并发：4*concurrent_num的效果
    # concurrent_num和qps的关系：https://funboost.readthedocs.io/zh/latest/articles/c3.html#boost-concurrent-num-qps
    # concurrent_num 单个work里线程池并发数量，值是线程/协程数量.该值决定了从队列里一次性取出多少个任务，
    # 从消息中间件预取出的消息过多，造成python内存大、单个消费者掏空消息队列中间件造成别的新启动的消费者无任务可消费、
    # 对于不支持消费确认类型的中间件的随意重启会丢失大量正在运行的任务等不利影响。
    concurrent_num = 50

    # 该值是将所有消费者视为一个整体，每秒执行的函数次数。qps是优先于concurrent_num，但受到concurrent_num的约束
    # 指定1秒内的函数执行次数，例如可以是小数0.01代表每100秒执行一次，也可以是50代表1秒执行50次.为0则不控频。
    # 如果设置 concurrent_num = 1000(或100万)  qps = 10，那么一秒钟会执行10次func函数。如果不指定qps的值，则不进行控频，消费框架会平均每秒钟会执行50次函数func。
    # 如设置concurrent_num=1000，qps为1，则整个系统会自能控制调节线程池大小，确保每秒的执行1次函数，但总线程数量上限不会超过concurrent_num * work
    # 如果设置concurrent_num=5，qps=10，以此来达到每秒执行10次是不成立的，系统将以并发数=5运行。
    # 设置 concurrent_num = 1  qps = 100，那会如何呢？
    # 由于你设置的并发是1,对于一个需要2秒运行完成的函数，显然平均每2秒才能执行1次，就是框架真正的只能达到0.5个qps而不是100。
    # 所以 concurrent_num 和 qps，既有关系，也不是绝对的关系。
    # qps控频：https://funboost.readthedocs.io/zh/latest/articles/c4.html#qps
    qps: float = 0

    specify_concurrent_pool = None  # 使用指定的线程池（协程池），可以多个消费者共使用一个线程池，不为None时候。threads_num失效，具体看文档
    specify_async_loop = None  # 指定的async的loop循环，设置并发模式为async才能起作用。

    # 是否使用分布式空频（依赖redis统计消费者数量，然后自动调度每台电脑的频率，尽可能平分），默认是基于单个进程的控频。用这个功能必须配置好redis链接。
    """@boost中指定is_using_distributed_frequency_control = True
    则启用分布式全局控频，是跨进程跨python解释器跨服务器的全局控频。否则是基于当前消费者的控频。
    例如
    你设置的qps是100，is_using_distributed_frequency_control=False，run_consume.py脚本中启动fun.consume() 
    如果你反复启动5次这个run_consume.py或者执行5次fun.consume()，那么当做5个独立的消费者运行，频率总共会达到500次每秒，因为你部署了5个脚本。
    同理你如果用fun.multi_process_consume(4)启动了4个进程消费，那么就是4个消费者，总qps也会达到400次每秒
    如果设置了 is_using_distributed_frequency_control=True，那就会使用每个消费者发送到redis的心跳来统计总消费者个数。
    如果你部署了2次，那么每个消费者会平分qps，每个消费者是变成50qps，总共100qps。
    如果你部署了5次，那么每个消费者会平分qps，每个消费者是变成20qps，总共100qps。
    如果你中途关闭2个消费者，变成了3个消费者，每个消费者是变成 33.33qps，总共100qps。(框架qps支持小数，0.1qps表示每10秒执行1次)
    """
    is_using_distributed_frequency_control = False
    is_send_consumer_hearbeat_to_redis = True  # 是否将发布者的心跳发送到redis，有些功能的实现需要统计活跃消费者。因为有的中间件不是真mq。
    max_retry_times = 3  # 最大自动重试次数，当函数发生错误，立即自动重试运行n次，对一些特殊不稳定情况会有效果。
    consumin_function_decorator = None  # 函数的装饰器。因为此框架做参数自动转指点，需要获取精准的入参名称，不支持在消费函数上叠加 @ * args ** kwargs的装饰器，如果想用装饰器可以这里指定。
    # 超时秒数，函数运行超过这个时间，则自动杀死函数。为0是不限制。设置后代码性能会变差(尤其是任务内有多次函数调用)，非必要不要轻易设置。
    # 原因是__KThread(target=fun2, args=("Funboost", ))里的sys.settrace(self.globaltrace)会追踪每一个函数调用
    function_timeout = 0
    log_level = 20  # 框架的日志级别。logging.DEBUG(10)  logging.DEBUG(10) logging.INFO(20) logging.WARNING(30) logging.ERROR(40) logging.CRITICAL(50)
    logger_prefix = ''  # 日志前缀，可使不同的消费者生成不同的日志前缀
    create_logger_file = True  # 是否创建文件日志，文件日志的文件夹位置由 nb_log_config 中的 LOG_PATH 决定
    is_show_message_get_from_broker = False  # 从中间件取出消息时候时候打印显示出来
    is_print_detail_exception = True  # 是否打印详细的堆栈错误。为0则打印简略的错误占用控制台屏幕行数少。
    # 消息过期时间，为0永不过期，为10则代表，10秒之前发布的任务如果现在才轮到消费则丢弃任务。
    # 丢弃并不会通知业务，所以这个功能有点鸡肋。
    # 需要关闭该功能，并改写ap.push_for_apscheduler_use_db函数，设置消息产生时间，在接收到消息时判断是否已经超过了指定时间。
    msg_expire_senconds = 0     # 消息过期时间，秒。注意，主进程直接抛出异常，函数内部无法感知该事件，不建设使用该功能，业务内自行实现。
    do_task_filtering = False  # 是否执行基于函数参数的任务过滤，用这个功能必须配置好redis链接。
    '''
    task_filtering_expire_seconds是任务过滤的失效期，为0则永久性过滤任务。例如设置过滤过期时间是1800秒 ，
    30分钟前发布过1 + 2 的任务，现在仍然执行，
    如果是30分钟以内发布过这个任务，则不执行1 + 2，现在把这个逻辑集成到框架，一般用于接口价格缓存。
    '''
    task_filtering_expire_seconds = 0
    function_result_status_persistance_conf = FunctionResultStatusPersistanceConfig(False, False,
                                                                                    7 * 24 * 3600)  # 配置。是否保存函数的入参，运行结果和运行状态到mongodb。
    user_custom_record_process_info_func = None     # 任务消费结果的钩子函数，可以对结果进行处理 func_result(result: FunctionResultStatus)
    is_using_rpc_mode = False  # 是否使用rpc模式，可以在发布端获取消费端的结果回调，但消耗一定性能，使用async_result.result时候会等待阻塞住当前线程。用这个功能必须配置好redis链接
    is_do_not_run_by_specify_time_effect = False  # # 是否使不运行的时间段生效
    do_not_run_by_specify_time = ('10:00:00', '22:00:00')
    schedule_tasks_on_main_thread = False  # 直接在主线程调度任务，意味着不能直接在当前主线程同时开启两个消费者。fun.consume()就阻塞了，这之后的代码不会运行
    # 中间件种类，支持30种消息队列。 入参见 BrokerEnum枚举类的属性。
    # 中间件选型见3.1章节 https://funboost.readthedocs.io/zh/latest/articles/c3.html
    # REDIS 是最不靠谱的会丢失消息。funboost会一次性取出队列所有消息放到内存，而不是一次消费一个，重启服务会丢失消息
    # REDIS_ACK_ABLE 、 REDIS_STREAM(推荐)、 RedisBrpopLpush BrokerKind 这三种都是实现了确认消费。
    # 必须是5.0版本以上redis服务端才能支持  stream 数据结构
    broker_kind: int = BrokerEnum.REDIS_STREAM
# *********************************************** 以上是 boost装饰器的默认全局配置 *******************************************
