# coding:utf-8
# 模拟一个进城池 线程池，可以向里面添加任务，

import threading
import time
import queue
import random


def write_log(debug_name,err_message):
    import os
    import sys
    import pathlib
    from loguru import logger
    relpath = pathlib.Path(__file__).parent  
    log_path = relpath.joinpath('../../../logs/webscan.log')  #记录日志路径
    stdout_fmt = '<cyan>{time:HH:mm:ss,SSS}</cyan> ' \
                 '[<level>{level: <5}</level>] ' \
                 '<blue>{module}</blue>:<cyan>{line}</cyan> - ' \
                 '<level>{message}</level>'
    # # 日志文件记录格式
    logfile_fmt = '<light-green>{time:YYYY-MM-DD HH:mm:ss,SSS}</light-green> ' \
                  '[<level>{level: <5}</level>] ' \
                  '<cyan>{process.name}({process.id})</cyan>:' \
                  '<cyan>{thread.name: <10}({thread.id: <5})</cyan> | ' \
                  '<blue>{module}</blue>.<blue>{function}</blue>:' \
                  '<blue>{line}</blue> - <level>{message}</level>'

    #log_path = result_save_path.joinpath('webscan.log')
    

    logger.remove()
    logger.level(name='TRACE', no=5, color='<cyan><bold>', icon='✏️')
    logger.level(name='DEBUG', no=10, color='<blue><bold>', icon='🐞 ')
    logger.level(name='INFO', no=20, color='<green><bold>', icon='ℹ️')
    logger.level(name='ALERT', no=30, color='<yellow><bold>', icon='⚠️')
    logger.level(name='ERROR', no=40, color='<red><bold>', icon='❌️')
    logger.level(name='FATAL', no=50, color='<RED><bold>', icon='☠️')

    if not os.environ.get('PYTHONIOENCODING'):  # 设置编码
        os.environ['PYTHONIOENCODING'] = 'utf-8'

    logger.add(sys.stderr, level='INFO', format=stdout_fmt, enqueue=True)
    logger.add(log_path, level='DEBUG', format=logfile_fmt, enqueue=True,
               encoding='utf-8')
    logger.log(debug_name,err_message)


class threadpool:

    def __init__(self,threadnum,func_scan):
        self.thread_count = self.thread_nums = threadnum
        self.thread_count_lock = threading.Lock()
        self.load_lock = threading.Lock()
        self.isContinue = True
        self.func_scan = func_scan
        self.queue = queue.Queue()

    def push(self,payload):
        self.queue.put(payload)


    def changeThreadCount(self,num):
        self.thread_count_lock.acquire()
        self.thread_count += num
        self.thread_count_lock.release()

    def run(self):
        for i in range(self.thread_nums):
            t = threading.Thread(target=self.scan)
            t.setDaemon(True)
            t.start()
        while 1:
            if self.thread_count > 0 and self.isContinue:
                time.sleep(0.3)
            else:
                break
    def stop(self):
        self.load_lock.acquire()
        self.isContinue = False
        self.load_lock.release()
        
    def scan(self):
        while 1:
            self.load_lock.acquire()
            if self.queue.qsize() > 0 and self.isContinue:
                payload = self.queue.get()
                self.load_lock.release()
            else:
                self.load_lock.release()
                break
            try:
                # POC在执行时报错如果不被处理，线程框架会停止并退出
                self.func_scan(payload)
                time.sleep(0.5)
            except KeyboardInterrupt:
                self.isContinue = False
                raise KeyboardInterrupt
            except Exception as e:
                write_log('ERROR','线程模块'+str(self.func_scan)+'错误:'+str(e))

        self.changeThreadCount(-1)


if __name__ == '__main__':
    def calucator(num):
        i = random.randint(1, 100)
        u = num
        a = i * u
        if (a % 6 == 0):
            for x in range(5):
                print("new thread")
                # p.push(x)

    p = threadpool(3, calucator)
    for i in range(100000):
        p.push(i)
    p.run()


