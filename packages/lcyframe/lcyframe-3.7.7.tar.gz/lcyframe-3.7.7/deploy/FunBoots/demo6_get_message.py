from funboost import boost
import time

@boost('test_queue77g', log_level=10, broker_kind=BrokerEnum.REDIS_ACK_ABLE, qps=5,
       create_logger_file=False,is_show_message_get_from_broker=True,concurrent_mode=ConcurrentModeEnum.SINGLE_THREAD
       # specify_concurrent_pool= pool2,
       # concurrent_mode=ConcurrentModeEnum.SINGLE_THREAD, concurrent_num=3,is_send_consumer_hearbeat_to_redis=True,function_timeout=10,
       # function_result_status_persistance_conf=FunctionResultStatusPersistanceConfig(True,True)
       )
def f2(a, b):
    time.sleep(10)
    print(a, b)
    return a - b


if __name__ == '__main__':
    f2.clear()
    for i in range(8):
        f2.push(i, i * 5)
    print(f2.get_message_count())

    f2.clear()
    for i in range(20):
        f2.push(i, i * 2)
    print(f2.get_message_count())


    # fff.clear()     # 清空消息队列
    # fff.get_message_count()  # 获取消息队中的消息数量，
    # fff.get_message_count() = 0
    # 不能使用来判断消息队列没任务了以为该函数的所有消息被消费完成了，本地内存队列存储了
    # 一部分消息和正在执行的也有一部分消息，如果要判断消费完成了，应该使用4.17章节的判断函数运行完所有任务，再执行后续操作。