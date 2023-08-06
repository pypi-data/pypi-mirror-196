import time, random
from deploy.celery.start import app
from celery.exceptions import SoftTimeLimitExceeded

@app.task
def timeout_demo():
    """
    celery_config.py配置文件设置
    celery任务执行结果的超时时间，超时后抛出异常
    CELERY_TASK_RESULT_EXPIRES = 1200
    """
    try:
        pass
    except SoftTimeLimitExceeded:
        print("运行超时")