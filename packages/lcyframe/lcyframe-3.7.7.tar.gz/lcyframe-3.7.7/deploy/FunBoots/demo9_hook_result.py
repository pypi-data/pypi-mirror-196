from funboost import boost, FunctionResultStatus

"""
钩子函数：任务消费结果的钩子函数，可以对结果进行处理
用户自定义记录函数消费 状态/结果
可以通过设置 user_custom_record_process_info_func 的值指向你的函数，来记录函数的消费结果，这种比较灵活。
用户定义一个函数，函数的入参只有一个 function_result_status ，这个变量是 FunctionResultStatus 类型的对象，有很多属性可供使用，
例如函数 入参 结果 耗时 发布时间 处理线程id 处理机器等等，可以更好的和用户自己的系统对接。

测试用户自定义记录函数消息处理的结果和状态到mysql

"""


def my_save_process_info_fun(function_result_status: FunctionResultStatus):
    """
    钩子函数，在任务运行完毕后调用（如果有重试，则先执行所有重试次数）
    function_result_status变量上有各种丰富的信息 ,用户可以使用其中的信息
    用户自定义记录函数消费信息的钩子函数
    <class 'funboost.consumers.base_consumer.FunctionResultStatus'>
    {
        "queue_name": "engine_wam_task",
        "function": "engine_wam_task",
        "msg_dict": {
                "task_id": 2,
                "url": "www.baidu.com",
                "task_at": 1673940982.2605052,
                "extra": {
                    "task_id": "engine_wam_task_result:9431d6bc-d716-4e9e-99fc-b1cc6610dcd8",
                    "publish_time": 1673940982.2606,
                    "publish_time_format": "2023-01-17 15:36:22"
                }
        },
        "task_id": "engine_wam_task_result:9431d6bc-d716-4e9e-99fc-b1cc6610dcd8",
        "process_id": 13905,
        "thread_id": 123145697210368,
        "publish_time": 1673940982.2606,
        "publish_time_str": "2023-01-17 15:36:22",
        "params": {
            "task_id": 2,
            "url": "www.baidu.com",
            "task_at": 1673940982.2605052
            },
        "params_str": "{\"task_id\": 2, \"url\": \"www.baidu.com\", \"task_at\": 1673940982.2605052}",
        "result": null,
        "run_times": 1,
        "exception": null,
        "time_start": 1674867846.6369522,
        "time_cost": 335.296,
        "time_end": 1674868181.9326432,
        "success": true,        # 注意，消费内部抛出异常时，该值也为true
        "total_thread": 16,
        "has_requeue": false,
        "host_name": "Mac",
        "host_process": "Mac - 13905",
        "script_name": "funboost_server.py",
        "script_name_long": "/Users/apple/www/caih/caihcsp-engine/Server/scheduler/funboost_server.py",
        "insert_time_str": "2023-01-28 09:09:41",
        "insert_minutes": "2023-01-28 09:09",
        "insert_time": "2023-01-28 09:09:41",
        "utime": "2023-01-28 01:09:41",
        "_id": "engine_wam_task_result:9431d6bc-d716-4e9e-99fc-b1cc6610dcd8"
    }
    """
    print('function_result_status变量上有各种丰富的信息: ',
          function_result_status.publish_time, function_result_status.publish_time_str,
          function_result_status.params, function_result_status.msg_dict,
          function_result_status.time_cost, function_result_status.result,
          function_result_status.process_id, function_result_status.thread_id,
          function_result_status.host_process, )
    print('保存到数据库', function_result_status.get_status_dict())

# user_custom_record_process_info_func=my_save_process_info_fun 设置记录函数消费状态的钩子
@boost('test_user_custom', user_custom_record_process_info_func=my_save_process_info_fun)
def f(x):
    print(x * 10)


if __name__ == '__main__':
    for i in range(50):
        f.push(i)
    print(f.publisher.get_message_count())
    f.consume()