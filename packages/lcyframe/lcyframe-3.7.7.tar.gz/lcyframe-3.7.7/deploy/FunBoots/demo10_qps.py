"""
演示框架的qps控频功能

此框架对函数耗时随机波动很大的控频精确度达到96%以上

此框架对耗时恒定的函数控频精确度达到99.9%

在指定rate_limit 超过 20/s 时候，celery对耗时恒定的函数控频精确度60%左右，下面的代码会演示这两个框架的控频精准度对比。

此框架针对不同指定不同qps频次大小的时候做了不同的三种处理方式。
框架的控频是直接基于代码计数，而非使用redis 的incr计数，因为python操作一次redis指令要消耗800行代码左右，
如果所有任务都高频率incr很消耗python脚本的cpu也对redis服务端产生灾难压力。
例如假设有50个不同的函数，分别都要做好几千qps的控频，如果采用incr计数，光是incr指令每秒就要操作10万次redis，
所以如果用redis的incr计数控频就是个灾难，redis incr的计数只适合 1到10大小的qps，不适合 0.01 qps 和 1000 qps这样的任务。

同时此框架也能很方便的达到 5万 qps的目的，装饰器设置qps=50000 和 is_using_distributed_frequency_control=True,
然后只需要部署很多个进程 + 多台机器，框架通过redis统计活跃消费者数量，来自动调节每台机器的qps，框架的分布式控频开销非常十分低，
因为分布式控频使用的仍然不是redis的incr计数，而是基于每个消费者的心跳来统计活跃消费者数量，然后给每个进程分配qps的，依然基于本地代码计数。

例如部署100个进程(如果机器是128核的，一台机器足以，或者20台8核机器也可以)
以20台8核机器为例子，如果把机器减少到15台或增加机器到30台，随便减少部署的机器数量或者随便增加机器的数量，
代码都不需要做任何改动和重新部署，框架能够自动调节来保持持续5万次每秒来执行函数，不用担心部署多了30台机器，实际运行qps就变成了10几万。
(前提是不要把机器减少到10台以下，因为这里假设这个函数是一个稍微耗cpu耗时的函数，要保证所有资源硬件加起来有实力支撑5万次每秒执行函数)

每台机器都运行 test_fun.multi_process_conusme(8)，只要10台以上1000台以下随意随时随地增大减小运行机器数量，
代码不需要做任何修改变化，就能很方便的达到每秒运行5万次函数的目的。

qps控频和自适应扩大和减小并发数量。
通过不同的时间观察控制台，可以发现无论f2这个函数需要耗时多久（无论是函数耗时需要远小于1秒还是远大于1秒），框架都能精确控制每秒刚好运行2次。
当函数耗时很小的时候，只需要很少的线程就能自动控制函数每秒运行2次。
当函数突然需要耗时很大的时候，智能线程池会自动启动更多的线程来达到每秒运行2次的目的。
当函数耗时从需要耗时很大变成只需要耗时很小的时候，智能线程池会自动缩小线程数量。
总之是围绕qps恒定，会自动变幻线程数量，做到既不多开浪费cpu切换，也不少开造成执行速度慢。
"""
import time
import threading
from funboost import boost, BrokerEnum, ConcurrentModeEnum

t_start = time.time()


@boost('queue_test2_qps', qps=2, broker_kind=BrokerEnum.PERSISTQUEUE, concurrent_mode=ConcurrentModeEnum.THREADING,
       concurrent_num=600)
def f2(a, b):
    """
    这个例子是测试函数耗时是动态变化的，这样就不可能通过提前设置参数预估函数固定耗时和搞鬼了。看看能不能实现qps稳定和线程池自动扩大自动缩小
    要说明的是打印的线程数量也包含了框架启动时候几个其他的线程，所以数量不是刚好和所需的线程计算一样的。
    """
    result = a + b
    sleep_time = 0.01
    if time.time() - t_start > 60:  # 先测试函数耗时慢慢变大了，框架能不能按需自动增大线程数量
        sleep_time = 7
    if time.time() - t_start > 120:
        sleep_time = 30
    if time.time() - t_start > 240:  # 最后把函数耗时又减小，看看框架能不能自动缩小线程数量。
        sleep_time = 0.8
    if time.time() - t_start > 300:
        sleep_time = None
    print(
        f'{time.strftime("%H:%M:%S")}  ，当前线程数量是 {threading.active_count()},   {a} + {b} 的结果是 {result}， sleep {sleep_time} 秒')
    if sleep_time is not None:
        time.sleep(sleep_time)  # 模拟做某事需要阻塞n秒种，必须用并发绕过此阻塞。
    return result


if __name__ == '__main__':
    f2.clear()
    for i in range(1000):
        f2.push(i, i * 2)
    f2.consume()