"""
7.8.2 gevent/eventlet 和 asyncio 用法区别感受
https://function-scheduling-distributed-framework.readthedocs.io/zh_CN/latest/articles/c7.html#gevent-eventlet-asyncio

比方说汽车的自动挡和手动挡，学了手动挡一定会开自动挡，只学自动挡很难开手动挡。
asyncio方式的代码比正常普通同步思维的代码写法也要难得多了，能玩asyncio的人一定会用threading gevent，
但只用过threading gevent，不去专门学习asyncio的用法，100%是玩不转的。

gevent就像自动挡汽车，自动换挡相当于自动切换阻塞。
asyncio就像手动挡，全要靠自己写 await / async def /loop / run_until_complete /run_forever/
run_coroutine_threadsafe /wait / wait_for /get_event_loop / new_event_loop / get_running_loop
,写法很麻烦很难。异步多了一个loop就像手动挡汽车多了一个离合器一样，十分之难懂。

手动挡玩的溜性能比自动挡高也更省油。asyncio玩的溜那么他的io并发执行速度和效率也会更好，cpu消耗更少。
如果你写一般的代码，那就用同步方式思维来写吧，让分布式函数调度框架来替你自动并发就可以啦。
如果追求更好的控制和性能，不在乎代码写法上的麻烦，并且asyncio技术掌握的很溜，那就用asyncio的方式吧。
"""

from funboost import boost, ConcurrentModeEnum
@boost("task_queue_name", concurrent_mode=ConcurrentModeEnum.ASYNC)
async def async_name():
    """
    这种方式是@boost装饰在async def定义的函数上面。
    celery不支持直接调度执行async def定义的函数，但此框架是直接支持asyncio并发的。
    """
    pass

