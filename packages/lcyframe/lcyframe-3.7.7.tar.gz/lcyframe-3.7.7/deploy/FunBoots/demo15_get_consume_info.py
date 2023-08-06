"""
4.13 跨python项目怎么发布任务或者获取函数执行结果？
别的语言项目或者别的python项目手动发布消息到中间件，让分布式函数调度框架消费任务，
例如项目b中有add函数，项目a里面无法 import 导入这个add 函数。

1)第一种方式，使用能操作消息中间件的python包，手动发布任务到消息队列中间件
如果是别的语言发布任务，或者python项目a发布任务但是让python项目b的函数去执行，可以直接发布消息到中间件里面。
手动发布时候需要注意 中间件类型 中间件地址 队列名 @boost和funboost_config.py指定的配置要保持一致。
需要发布的消息内容是 入参字典转成json字符串，然后发布到消息队列中间件。
以下以redis中间件为例子。演示手动发布任务到中间件。
"""
from redis import Redis
import time, json
from funboost import boost, BrokerEnum
@boost('test_queue668', broker_kind=BrokerEnum.REDIS)
def add(x, y):
    print(f'''  计算  {x} + {y} = {x + y}''')
    time.sleep(4)
    return x + y


if __name__ == '__main__':
    r = Redis(db=7, host='127.0.0.1')
    for i in range(10):
        add.push(i, i * 2)  # 正常同一个python项目是这么发布消息,使用函数.push或者publish方法
        r.lpush('test_queue668', json.dumps({'x': i, 'y': i * 2}))  # 不同的项目交互，可以直接手动发布消息到中间件

"""
第二种方式，使用伪函数来作为任务,只写函数声明不写函数体。
此方式是一名网友的很机智的建议，我觉得可行。
例如还是以上面的求和函数任务为例，在项目a里面可以定义一个假函数声明,并且将b项目的求和add函数装饰器复制过去，但函数体不需要具体内容
之后通过这个假的add函数就可以享受到与在同一个项目中如何正常发布和获取求和函数的执行结果 一模一样的写法方式了。
例如add.clear() 清空消息队列，add.push发布,add.publish发布，async_result.get获取结果，都可以正常使用， 但不要使用add.consume启动消费，因为这个是假的函数体，不能真正的执行求和.
"""

@boost('test_queue668', broker_kind=BrokerEnum.REDIS)  # a项目里面的这行和b项目里面的add函数装饰器保持一致。
def add(x, y):  # 方法名可以一样，也可以不一样，但函数入参个数 位置 名称需要保持不变。
    pass  # 方法体，没有具体的求和逻辑代码，只需要写个pass就行了。
