
"""
有的人动态生成消费者，queue_name或者其他装饰器入参是动态的，无法在代码里面提前写死。可以这样。

最开始框架就没有装饰器，一开始是这么使用的get_consumer，利用工厂模式生成不同中间件类型的消费者。这个更接近本质使用。
boost装饰器使用方式是在后来时候才设计加上的。
"""
from funboost import get_consumer, BrokerEnum


def add(a, b):
    print(a + b)

# 工厂模式返回一个消费者
# 非装饰器方式，多了一个入参，需要手动指定consuming_function入参的值。
consumer = get_consumer('queue_test_f01', consuming_function=add, qps=0.2, broker_kind=BrokerEnum.REDIS_ACK_ABLE)

if __name__ == '__main__':
    for i in range(10, 20):
        consumer.publisher_of_same_queue.publish(dict(a=i, b=i * 2))  # consumer.publisher_of_same_queue.publish 发布任务
    consumer.start_consuming_message()  # 使用consumer.start_consuming_message 消费任务