from demo1 import fff, task_fun
"""
生产者
"""
if __name__ == "__main__":
    for i in range(1):
        # fff.pub(dict(x=i))    # 使用add.pub 发布任务
        fff.push(i)             # 发布者发布任务

        # 这个与push相比是复杂的发布，第一个参数是函数本身的入参字典，后面的参数为任务控制参数，例如可以设置task_id，设置延时任务，设置是否使用rpc模式等。
        # fff.publish({'x': i * 10, 'y': i * 2},
        #             priority_control_config=PriorityConsumingControlConfig(countdown=1,
        #                                                                    misfire_grace_time=15
        #                                                                    )
        #             )

    # for i in range(100):
    #     task_fun.push(i, y=i * 2)  # 发布者发布任务