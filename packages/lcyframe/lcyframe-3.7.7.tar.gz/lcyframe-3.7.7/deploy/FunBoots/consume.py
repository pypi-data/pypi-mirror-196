from demo1 import fff, task_fun

if __name__ == "__main__":
    # 可以连续多个两个消费者，因为conusme是启动独立线程里面while 1调度的，不会阻塞主线程，所以可以连续运行多个启动消费。
    fff.consume()                           # 主进程内，启动循环调度并发消费任务
    # fff.start()  # 和 conusme()等效
    # fff.multi_process_consume(2)            # 再启动6个单独进程叠加多线程。这个是新加的方法，细粒度 线程 协程并发 同时叠加8个进程，速度炸裂。主要是无需导入run_consumer_with_multi_process函数。
    # print("以上代码运行后，我并不会被阻塞")
    # run_consumer_with_multi_process(f,8)   # 这个是细粒度 线程 协程并发 同时叠加8个进程，速度炸裂。

    # task_fun.consume()  # 消费者启动循环调度并发消费任务

    # fff.clear()     # 清空消息队列
    # fff.get_message_count()  # 获取消息队中的消息数量，
    # fff.get_message_count() = 0
    # 不能使用来判断消息队列没任务了以为该函数的所有消息被消费完成了，本地内存队列存储了
    # 一部分消息和正在执行的也有一部分消息，如果要判断消费完成了，应该使用4.17章节的判断函数运行完所有任务，再执行后续操作。

    # 判断已经把所有任务都执行完毕
    # import os, sys
    # from funboost import wait_for_possible_has_finish_all_tasks_by_conusmer_list
    # if wait_for_possible_has_finish_all_tasks_by_conusmer_list(minutes=3):
    #     """
    #     :param consumer_list: 多个消费者列表
    #     :param minutes: 消费者连续多少分钟没执行任务任务 并且 消息队列中间件中没有，就判断为消费完成。为了防止是长耗时任务，一般判断完成是真正提供的minutes的2个周期时间。
    #     :return:
    #     """
    #     sys.exit()