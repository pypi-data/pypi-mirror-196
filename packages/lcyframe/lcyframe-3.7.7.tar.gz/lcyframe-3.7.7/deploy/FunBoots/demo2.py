import time
from funboost import boost, BrokerEnum, get_consumer
'''
这是此框架最重要的一个函数，必须看懂里面的入参有哪些。
此函数的入参意义请查看 get_consumer的入参注释。

本来是这样定义的，def boost(queue_name, **consumer_init_kwargs):
为了更好的ide智能补全，重复写全函数入参。

装饰器方式注册消费任务，如果有人过于喜欢装饰器方式，例如celery 装饰器方式的任务注册，觉得黑科技，那就可以使用这个装饰器。
假如你的函数名是f,那么可以调用f.publish或f.pub来发布任务。调用f.start_consuming_message 或 f.consume 或 f.start消费任务。
必要时候调用f.publisher.funcxx   和 f.conusmer.funcyy。

装饰器版，使用方式例如：
'''
@boost('queue_test_f01', qps=0.2, broker_kind=2)
def f(a, b):
    print(a + b)

for i in range(10, 20):
    f.pub(dict(a=i, b=i * 2))
    f.push(i, i * 2)
f.consume()
# f.multi_process_conusme(8)             # # 这个是新加的方法，细粒度 线程 协程并发 同时叠加8个进程，速度炸裂。主要是无需导入run_consumer_with_multi_process函数。
# run_consumer_with_multi_process(f,8)   # 这个是细粒度 线程 协程并发 同时叠加8个进程，速度炸裂。

'''
常规方式，使用方式如下
装饰器版本的 boost 入参 和 get_consumer 入参99%一致，唯一不同的是 装饰器版本加在了函数上自动知道消费函数了，
所以不需要传consuming_function参数。
'''
def f(a, b):
    print(a + b)

consumer = get_consumer('queue_test_f01', consuming_function=f,qps=0.2, broker_kind=2)
# 需要手动指定consuming_function入参的值。
for i in range(10, 20):
    consumer.publisher_of_same_queue.publish(dict(a=i, b=i * 2))
consumer.start_consuming_message()