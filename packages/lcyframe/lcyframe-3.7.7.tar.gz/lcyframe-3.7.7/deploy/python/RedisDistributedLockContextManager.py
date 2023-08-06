import sys, uuid
from funboost.utils import LogManager, nb_print, LoggerMixin
from nb_log import LoggerLevelSetterMixin

class RedisDistributedLockContextManager(LoggerMixin, LoggerLevelSetterMixin):
    """
    分布式redis锁上下文管理.
    """

    def __init__(self, redis_client, redis_lock_key, expire_seconds=30, ):
        self.redis_client = redis_client
        self.redis_lock_key = redis_lock_key
        self._expire_seconds = expire_seconds
        self.identifier = str(uuid.uuid4())
        self.has_aquire_lock = False

    def __enter__(self):
        self._line = sys._getframe().f_back.f_lineno  # 调用此方法的代码的函数
        self._file_name = sys._getframe(1).f_code.co_filename  # 哪个文件调了用此方法
        self.redis_client.set(self.redis_lock_key, value=self.identifier, ex=self._expire_seconds, nx=True)
        identifier_in_redis = self.redis_client.get(self.redis_lock_key)
        if identifier_in_redis and identifier_in_redis.decode() == self.identifier:
            self.has_aquire_lock = True
        return self

    def __bool__(self):
        return self.has_aquire_lock

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.has_aquire_lock:
            self.redis_client.delete(self.redis_lock_key)
        if self.has_aquire_lock:
            log_msg = f'\n"{self._file_name}:{self._line}" 这行代码获得了redis锁 {self.redis_lock_key}'
            self.logger.debug(log_msg)
        else:
            log_msg = f'\n"{self._file_name}:{self._line}" 这行代码此次没有获得redis锁 {self.redis_lock_key}'
            self.logger.debug(log_msg)


if __name__ == '__main__':
    with RedisDistributedLockContextManager("redisconn", "lock_key") as lock:
        pass

    with RedisDistributedLockContextManager(redis_db_frame, lock_key, ) as lock:
        if lock.has_aquire_lock:
            self._distributed_consumer_statistics.send_heartbeat()
            current_queue_hearbeat_ids = self._distributed_consumer_statistics.get_queue_heartbeat_ids(
                without_time=True)
            xinfo_consumers = self.redis_db_frame_version3.xinfo_consumers(self._queue_name, self.GROUP)
            # print(current_queue_hearbeat_ids)
            # print(xinfo_consumers)
            for xinfo_item in xinfo_consumers:
                # print(xinfo_item)
                if xinfo_item['idle'] > 7 * 24 * 3600 * 1000 and xinfo_item['pending'] == 0:
                    self.redis_db_frame_version3.xgroup_delconsumer(self._queue_name, self.GROUP, xinfo_item['name'])
                if xinfo_item['name'] not in current_queue_hearbeat_ids and xinfo_item[
                    'pending'] > 0:  # 说明这个消费者掉线断开或者关闭了。
                    pending_msg_list = self.redis_db_frame_version3.xpending_range(
                        self._queue_name, self.GROUP, '-', '+', 1000, xinfo_item['name'])
                    if pending_msg_list:
                        # min_idle_time 不需要，因为加了分布式锁，所以不需要基于idle最小时间的判断，并且启动了基于心跳的确认消费助手，检测消费者掉线或关闭或断开的准确率100%。
                        xclaim_task_list = self.redis_db_frame_version3.xclaim(self._queue_name, self.GROUP,
                                                                               self.consumer_identification, force=True,
                                                                               min_idle_time=0 * 1000,
                                                                               message_ids=[task_item['message_id'] for
                                                                                            task_item in
                                                                                            pending_msg_list])
                        if xclaim_task_list:
                            self.logger.warning(
                                f' {self._queue_name}  的分组 {self.GROUP} 的消费者 {self.consumer_identification} 夺取 断开的消费者 {xinfo_item["name"]}'
                                f'  {len(xclaim_task_list)} 个任务，详细是 {xclaim_task_list} ')
                            for task in xclaim_task_list:
                                kw = {'body': json.loads(task[1]['']), 'msg_id': task[0]}
                                self._submit_task(kw)
