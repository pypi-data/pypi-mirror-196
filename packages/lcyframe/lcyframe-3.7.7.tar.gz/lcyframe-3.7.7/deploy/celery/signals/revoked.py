from celery.signals import task_revoked, after_task_publish
from deploy.celery.works.demo import add3




from celery.signals import task_revoked, after_task_publish

@after_task_publish.connect(sender=add3)
def task_sent_handler(sender=None, headers=None, body=None, **kwargs):
    # information about task are located in headers for task messages
    # using the task protocol version 2.
    info = headers if 'task' in headers else body
    print('after_task_publish for task id {info[id]}'.format(
        info=info,
    ))
    args = body[0]      # 对应传参方式：add3.apply_async((1, ))
    kw = body[1]        # 对应传参方式：add3.apply_async(kw={"x": 1})
    print(kw)



@task_revoked.connect(sender=add3)  # start_task 任务过期信号
def task_revoked_handler(sender=None, headers=None, body=None, **kwargs):
    """
    任务过期处理
    """
    print(111111111111111111)
    kw = kwargs.get("request").kwargs
    print(kw)

