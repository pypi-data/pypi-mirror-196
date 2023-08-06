import random, time, threading

"""
Python多线程（threading.Thread）的用法
https://www.jianshu.com/p/ebecd0667aee
python开发基础篇:六:多线程
https://www.cnblogs.com/yuanwt93/p/15886333.html
Python 并发简介（多线程、多进程）
https://blog.csdn.net/qingguideng/article/details/125399819
"""
class MyThread(threading.Thread):
    """
    监听任务执行情况，定期记录任务执行时间
    防止任务被杀死、超时后，无法判断任务当前状态
    ps: 调用该方法，务必设置任务的重试次数为0（max_retry_times=0），否则会频繁开启监听
    """
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, group=None, target=None, args=args, kwargs=kwargs)
        self.flag = True
        self.args = args

    def run(self):
        print(self.args, "子线程开始运行")
        n = 0
        while self.flag:
            time.sleep(3)
            print(self.args, "子线程正在执行任务")
            n += 1
            if n == 20:
                break
        print(self.args, "子线程已完成")

    def stop(self):
        self.flag = False

# t = threading.Thread(target=main_thread)
t = MyThread(random.randint(1, 100))
t.start()
time.sleep(10)
t.stop()
print("已通知子线程退出")
print("主线程退出")
