
from funboost import PriorityConsumingControlConfig
from demo9_rpc_work import add
"""
rpc回调结果在线程池中处理
客户端调用脚本，单线程发布阻塞获取两书之和的结果，执行求和过程是在服务端。 test_frame\test_rpc\test_publish.py
这种方式如果在主线程单线程for循环运行100次，因为为了获取结果，导致需要300秒才能完成100次求和。

"""

def show_result(status_and_result: dict):
    """
    :param status_and_result: 一个字典包括了函数入参、函数结果、函数是否运行成功、函数运行异常类型
    {
        'queue_name': 'test_rpc_queue',
        'function': 'add',
        'msg_dict': {
            'a': 94,
            'b': 188, '
            extra': {
                'task_id': 'test_rpc_queue_result:4f047b34-4600-4e60-a6e9-aff22b39d945',
                'publish_time': 1671076219.146,
                'publish_time_format': '2022-12-15 11:50:19'
                }
         },
         'task_id': 'test_rpc_queue_result:4f047b34-4600-4e60-a6e9-aff22b39d945',
         'process_id': 35217,
         'thread_id': 123147235528704,
         'publish_time': 1671076219.146,
         'publish_time_str': '2022-12-15 11:50:19',
         'params': {'a': 94, 'b': 188},
         'params_str': '{"a": 94, "b": 188}',
         'result': 282,
         'run_times': 1,
         'exception': None,
         'time_start': 1671076219.433548,
         'time_cost': 3.187,
         'time_end': 1671076222.620366,
         'success': True,
         'total_thread': 102,
         'has_requeue': False,
         'host_name': 'Mac',
         'host_process': 'Mac - 35217',
         'script_name': 'demo9_rpc_work.py',
         'script_name_long': '/Users/apple/www/lcyframepy3/deploy/FunBoots/demo9_rpc_work.py',
         'insert_time_str': '2022-12-15 11:50:22',
         'insert_minutes': '2022-12-15 11:50',
         '_id': 'test_rpc_queue_result:4f047b34-4600-4e60-a6e9-aff22b39d945'
    }
    """
    print(status_and_result["result"])

for i in range(100):
    async_result = add.push(i, i * 2)   # AsyncResult

    # 等待结果【阻塞】
    # async_result.set_timeout(3600)  # 这样设置后，就是为了获得消费结果，最大等待3600秒。 默认是最大等待120秒返回结果，如果消费函数本身耗时就需要消耗很长的时间，可以适当扩大这个时间。
    # print(async_result.result)  # 执行 .result是获取函数的运行结果，会阻塞当前发布消息的线程直到函数运行完成。

    # rpc获取结果【非阻塞】
    # 如果add函数的@boost装饰器参数没有设置 is_using_rpc_mode=True，则在发布时候也可以指定使用rpc模式。
    # async_result = add.publish(dict(a=i * 10, b=i * 20), priority_control_config=
    # PriorityConsumingControlConfig(is_using_rpc_mode=True))
    # print(async_result.status_and_result)

    # 异步回调等待结果【非阻塞】
    # async_result.set_callback(show_result)  # 使用回调函数在线程池中并发的运行函数结果

