import time
from funboost import boost

"""
暂停消费
框架支持暂停消费功能和继续消费功能，boost装饰器需要设置is_send_consumer_hearbeat_to_redis=True
"""

@boost('test_queue73ac', is_send_consumer_hearbeat_to_redis=True)
def f2(a, b):
    return a - b


if __name__ == '__main__':
    for i in range(1000):
        # f.push(i, i * 2)
        f2.push(i, i * 2)
    f2.consume()
    
    while 1:
        """
        f.continue_consume 意思是继续消费，这个设置redis对应键 f'funboost_pause_flag:{self.queue_name}' 的状态为1了，
        f.pause_consume 意思是暂停消费，这个设置redis对应键 f'funboost_pause_flag:{self.queue_name}' 的状态为0了，
        框架中有专门的线程每隔10秒扫描redis中设置的暂停状态判断是否需要暂停和继续消费，所以设置暂停和接续后最多需要10秒就能暂停或启动消费生效了。
        
        有的人问怎么在其他地方设置暂停消费，说我这例子是函数和设置暂停消费在同一个脚本，
        这个从redis获取暂停状态本来就是为了支持从python解释器外部或者远程机器设置暂停，怎么可能只能在函数所在脚本设置暂停消费。
        例如在脚本 control_pause.py中写
        from xx import f2
        f2.pause_consume()
        这不就完了吗。如果是别的java项目代码中控制暂停消费，可以设置redis的 funboost_pause_flag:{queue_name} 这个键的值为 1，
        这样就能使消费暂停了。在python web接口中设置暂停状态就用 f2.pause_consume() 就行了。
        """
        f2.pause_consume()
        time.sleep(300)
        f2.continue_consume()
        time.sleep(300)

