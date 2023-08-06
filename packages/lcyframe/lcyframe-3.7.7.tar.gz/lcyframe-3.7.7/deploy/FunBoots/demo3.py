import time
from funboost import boost, BrokerEnum

@boost('test_queue66c', qps=1/30,broker_kind=BrokerEnum.KAFKA_CONFLUENT)
def f(x, y):
    """
    超高速多进程发布，例如先快速发布1000万个任务到中间件，以后慢慢消费
    """
    print(f'函数开始执行时间 {time.strftime("%H:%M:%S")}')

if __name__ == '__main__':
    # 用法例如，快速20进程发布1000万任务，充分利用多核加大cpu使用率。
    f.multi_process_pub_params_list([{'x':i,'y':i*3}  for i in range(10000000)],process_num=20)
    f.consume()