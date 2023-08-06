"""
关于push、publish的区别
"""
def publish(self, msg: typing.Union[str, dict], task_id=None,
            priority_control_config: PriorityConsumingControlConfig = None):
    """

    :param msg:函数的入参字典或者字典转json。,例如消费函数是 def add(x,y)，你就发布 {"x":1,"y":2}
    :param task_id:可以指定task_id,也可以不指定就随机生产uuid
    :param priority_control_config:优先级配置，消息可以携带优先级配置，覆盖boost的配置。
    :return:
    """
    if isinstance(msg, str):
        msg = json.loads(msg)
    msg_function_kw = copy.copy(msg)
    if self.publish_params_checker:
        self.publish_params_checker.check_params(msg)
    task_id = task_id or f'{self._queue_name}_result:{uuid.uuid4()}'
    msg['extra'] = extra_params = {'task_id': task_id, 'publish_time': round(time.time(), 4),
                                   'publish_time_format': time.strftime('%Y-%m-%d %H:%M:%S')}
    if priority_control_config:
        # 覆盖boost全局参数，达到优先效果。最终会赋值给extra，所以业务函数是无法拿到这些优先参数的
        extra_params.update(priority_control_config.to_dict())
    t_start = time.time()
    decorators.handle_exception(retry_times=10, is_throw_error=True, time_sleep=0.1)(
        self.concrete_realization_of_publish)(json.dumps(msg, ensure_ascii=False))
    self.logger.debug(f'向{self._queue_name} 队列，推送消息 耗时{round(time.time() - t_start, 4)}秒  {msg_function_kw}')  # 显示msg太长了。
    with self._lock_for_count:
        self.count_per_minute += 1
        self.publish_msg_num_total += 1
        if time.time() - self._current_time > 10:
            self.logger.info(
                f'10秒内推送了 {self.count_per_minute} 条消息,累计推送了 {self.publish_msg_num_total} 条消息到 {self._queue_name} 队列中')
            self._init_count()
    return AsyncResult(task_id)

def push(self, *func_args, **func_kwargs):
    """
    简写，只支持传递消费函数的本身参数，不支持priority_control_config参数。
    类似于 publish和push的关系类似 apply_async 和 delay的关系。前者更强大，后者更简略。

    例如消费函数是
    def add(x,y):
        print(x+y)

    publish({"x":1,'y':2}) 和 push(1,2)是等效的。但前者可以传递priority_control_config参数。后者只能穿add函数所接受的入参。
    :param func_args:
    :param func_kwargs:
    :return:
    """
    # print(func_args,func_kwargs,self.publish_params_checker.all_arg_name)
    msg_dict = func_kwargs
    # print(msg_dict)
    # print(self.publish_params_checker.position_arg_name_list)
    # print(func_args)
    for index, arg in enumerate(func_args):
        # print(index,arg,self.publish_params_checker.position_arg_name_list)
        # msg_dict[self.publish_params_checker.position_arg_name_list[index]] = arg
        msg_dict[self.publish_params_checker.all_arg_name[index]] = arg
    # print(msg_dict)
    return self.publish(msg_dict)