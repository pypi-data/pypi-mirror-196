import time, random
from deploy.celery.start import app

# 我是消费者: 需启动进程 celery -A tasks worker --loglevel=info
@app.task  # 普通函数装饰为 celery task
def add(x):
    """
    seleep时间随机
    任务并发执行，谁先执行完毕，谁先输出结果
    :param x:
    :return:
    """
    n = random.random()
    time.sleep(n)
    # with open("w.txt", 'a') as p:
    #     p.write("%s:%s\n" % (x, n))
    print("task add: %s" % n)
    return x, n

@app.task
def add2(x):
    n = random.random()
    time.sleep(n)
    # with open("w.txt", 'a') as p:
    #     p.write("%s:%s\n" % (x, n))
    print("task add2: %s" % n)
    return x, n

@app.task
def add3(x):
    n = random.random()
    time.sleep(30)
    # with open("w.txt", 'a') as p:
    #     p.write("%s:%s\n" % (x, n))
    print("task add2: %s" % n)
    return x, n


if __name__ == '__main__':
    pass

    # shell启动
    # celery -A tasks worker --loglevel=info -n workername -Q celery    # -n 指定名称
    # celery worker -A  tasks.main -l info --autoscale=6,3 -Q default       # --autoscale=6,3 当work不够用时，自动再起3~6个work
    # celery -A proj worker --concurrency=4                                 # -c --concurrency并发运行指定数量的work
    # celery -A proj worker --concurrency=1000 -P eventlet                  # -P 指定loop的机制
    # celery -A celery_tasks.main beat -l info                              # 运行调度服务，Beat是调度器
    # celery --app=proj worker -l INFO
    # celery -A proj worker -l INFO -Q hipri,lopri
    # celery worker --autoscale=10,0

    # # pycharm Debug调试模式启动
    # from lcyframe.libs.singleton import CeleryCon
    # from lcyframe.celery_server import CeleryWorker
    # tasks = CeleryWorker()
    # app = CeleryCon._app  # 命令行模式运行：celery -A celery_start worker --loglevel=info --pool=eventlet --concurrency=10 -Qapp_queue
    # tasks.app = app
    # tasks.start()
