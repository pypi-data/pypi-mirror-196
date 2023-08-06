from celery.signals import (
    celeryd_init,
    celeryd_after_setup,
    worker_init,
    worker_process_init,
    worker_process_shutdown,
    worker_shutting_down
)

@celeryd_init.connect
def start_workers(sender=None, conf=None, **kwargs):
    """
    celery 主进程MainProcess启动前触发，
    即运行celery -A start worker --autoscale=1,4 --loglevel=INFO 时
    """
    print(11111)
    pass


@worker_init.connect
def worker_init(sender=None, conf=None, **kwargs):
    """
    紧跟celeryd_init后面触发
    celery主进程实例初始化时启动
    """
    print(2222)
    pass

@celeryd_after_setup.connect
def after_workers(sender=None, conf=None, **kwargs):
    """
    celery 主进程MainProcess启动后触发，
    """
    print(3333)
    pass

@worker_process_init.connect
def ForkPoolWorker_init(sender=None, conf=None, **kwargs):
    """
    celery 子进程ForkPoolWorker1~N启动后触发
    """
    print(4444)
    pass


@worker_shutting_down.connect
def MainProcess_shutdown_handler(sender=None, sig=None, how=None, **kwargs):
    """
    celery主进程MainProcess退出前触发（正常）
    注意：
    手动kill掉主进程MainProcess时（异常退出），不会触发该信号
    """
    print(55555)
    pass

@worker_process_shutdown.connect
def ForkPoolWorker_shutdown(sender=None, conf=None, **kwargs):
    """
    celery 子进程ForkPoolWorker1~N执行完成一次任务被销毁\退出前触发(正常退出)
    注意：
    手动kill掉主进程MainProcess时，由于主进程会主动把Fork出来的子进程正常退出，可以触发该信号
    手动kill掉子进程ForkPoolWorker1时（异常退出），不会触发该信号
    触发顺序在worker_shutting_down信号之后
    """
    print(66666)
    print(kwargs["pid"])
