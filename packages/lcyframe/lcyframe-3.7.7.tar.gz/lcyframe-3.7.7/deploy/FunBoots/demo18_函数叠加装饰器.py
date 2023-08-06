"""
框架支不支持函数上加两个装饰器？
由于发布任务时候需要自动精确组装入参字典，所以不支持  *args  **kwargs形式的入参，不支持叠加两个@装饰器
想在消费函数加装饰器，通过 boost 装饰器的 consumin_function_decorator 入参指定装饰器函数就行了。
那么如果是想叠加3个装饰器怎么写，例如本来想：

@boost('queue666')
@deco1('hello')
@deco2
def task_fun(x,y):
    ...

那就是写成 consumin_function_decorator=deco1('hello')(deco2) 就可以了，具体要了解装饰器的本质就知道，叠加100个装饰器都可以。
"""
# 如下的例子是使用redis的incr命令统计每台机器ip 总共运行了多少次函数。
import inspect
import nb_log
from funboost import boost
from funboost.utils import RedisMixin
from functools import wraps

def incr_deco(redis_key):
    def _inner(f):
        @wraps(f)
        def __inner(*args, **kwargs):
            result = f(*args, **kwargs)
            RedisMixin().redis_db_frame.incr(redis_key)
            # mongo_col.insert_one({'result':result,'args':str(args),'kwargs':str(kwargs)})
            return result

        return __inner

    return _inner


@boost('test_queue_235',consumin_function_decorator=incr_deco(nb_log.nb_log_config_default.computer_ip))
def fun(xxx, yyy):
    print(xxx + yyy)
    return xxx + yyy


if __name__ == '__main__':
    print(inspect.getfullargspec(fun))

    for i in range(10):
        fun.push(i, 2 * i)
    fun.consume()