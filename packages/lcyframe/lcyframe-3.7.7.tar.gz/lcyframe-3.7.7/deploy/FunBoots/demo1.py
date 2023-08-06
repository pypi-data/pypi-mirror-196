import time, os
from funboost import boost, BrokerEnum, get_consumer
from funboost import boost, BrokerEnum, ConcurrentModeEnum


@boost('test_multi_process_queue',broker_kind=BrokerEnum.REDIS_ACK_ABLE, concurrent_mode=ConcurrentModeEnum.THREADING,)
def fff(x):
    time.sleep(100)
    print(x, os.getpid())


@boost("task_queue_name1", qps=5)  # 入参包括20种，运行控制方式非常多，想得到的控制都会有。
def task_fun(x, y):
    print(f'{x} + {y} = {x + y}')
    time.sleep(3)  # 框架会自动并发绕开这个阻塞，无论函数内部随机耗时多久都能自动调节并发达到每秒运行 5 次 这个 task_fun 函数的目的。


# if __name__ == '__main__':
#     fff.multi_process_consume(6)  # 一次性启动6进程叠加多线程。
#     一次性运行所有消费者，前提是要把有@boost的python模块都import或者执行过
#     from funboost import boost_queue__fun_map
#     for queue_name, f in boost_queue__fun_map.items():
#         f.consume()

# if __name__ == "__main__":
#     for i in range(1):
#         task_fun.push(i, y=i * 2)  # 发布者发布任务
#     task_fun.consume()  # 消费者启动循环调度并发消费任务