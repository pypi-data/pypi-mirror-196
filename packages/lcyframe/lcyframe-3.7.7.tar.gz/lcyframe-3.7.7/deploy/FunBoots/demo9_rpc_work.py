import time
from funboost import boost, BrokerEnum
from funboost import boost, FunctionResultStatusPersistanceConfig

"""
演示rpc模式，即客户端调用远程函数并及时得到结果。
如果在发布端要获取消费端的执行结果，有两种方式
1、需要在@boost设置is_using_rpc_mode=True，默认是False不会得到结果。
2、如果@boost没有指定，也可以在发布任务的时候，用publish方法并写上
async_result = add.publish(dict(a=i * 10, b=i * 20), priority_control_config=
PriorityConsumingControlConfig(is_using_rpc_mode=True))
"""

@boost('test_rpc_queue', is_using_rpc_mode=True, broker_kind=BrokerEnum.REDIS_ACK_ABLE, concurrent_num=200,
       function_result_status_persistance_conf=FunctionResultStatusPersistanceConfig(True, True, 7 * 24 * 3600))
def add(a, b):
    time.sleep(3)
    return a + b


if __name__ == '__main__':
    add.consume()
    result = add.push(1, 2)
    print(1)        # 不会被阻塞
    print(result.result)