import os, sys, time, datetime
project_dir = os.path.dirname(__file__)
sys.path.append(os.path.dirname(project_dir))
sys.path.append(project_dir)
from apscheduler.schedulers.base import STATE_STOPPED, STATE_RUNNING, EVENT_ALL
from scheduler_listener.events import event_callback, main_event_resume
from scheduler.common.base import sc, default_task, MyCronTrigger, redis
from scheduler.common import constant
from scheduler.common.utils import scpprint
from publisher import push_for_apscheduler_use_db
from saas import models

def reload_task(clear=True):
    if clear:
        sc.remove_all_jobs()                          # 删除数据库中所有已配置的定时任务
    sc.add_job(default_task, 'interval', seconds=60, id="default_task", name="default_task", replace_existing=True)
    # sc.add_job(push_for_apscheduler_use_db,
    #            'date',
    #             run_date=datetime.datetime.now()+datetime.timedelta(seconds=10),
    #             id="restart_server", name="restart_server",
    #             args=('funboost_tasks.system', 'restart_server'),
    #             kwargs={
    #               "server_name": "funboost"
    #           },
    #            replace_existing=True)
    # sc.add_job(push_for_apscheduler_use_db,
    #            'date',
    #            run_date=datetime.datetime.now() + datetime.timedelta(seconds=10),
    #            id="demo", name="demo",
    #            args=('funboost_tasks.demo', 'consume_func'),
    #            kwargs={
    #                "x": 1,
    #                "y": 2,
    #            },
    #            replace_existing=True)

    # 读取tasks任务表
    status_items = [models.Tasks.STATUS_NEW, models.Tasks.STATUS_DONE, models.Tasks.STATUS_FAILED]
    tasks = models.Tasks.objects.filter(**{"is_delete": False,  "enable": 1,  "status__in": status_items})
    # for task in tasks:
    #     sc.add_job(push_for_apscheduler_use_db,
    #                MyCronTrigger.my_from_crontab("* * * * * * *"),
    #                id=str(task.id), name="任务监控:" + task.taskname or "任务名未定义",
    #                args=('funboost_tasks.task', 'engine_main_task'),
    #                kwargs={"task_id": task.id},
    #                replace_existing=True)

    # 读取wam任务表
    tasks = models.WAMTasks.objects.filter(**{"is_delete": False, "enable": 1})
    for task in tasks:
        if task.engine_status == models.WAMTasks.ENGINE_STATUS_ING:
            continue
        sc.add_job(push_for_apscheduler_use_db,
                   MyCronTrigger.my_from_crontab("* * * * * * *"),
                   id=str(task.id), name="可用性:" + task.taskname or "任务名未定义",
                   args=('funboost_tasks.wam', 'engine_wam_task'),
                   kwargs={"task_id": task.id, "url": task.url},
                   replace_existing=True)

def loop_event():
    scpprint("========== 调度引擎启动成功,持续监听事件 ==========")
    while bool(redis.blpop(constant.SCHE_LISTEN_KEY) or True):    # 监听新事件
        scpprint("监听到新的调度事件，正在操作读取指令...")
        time.sleep(1)
        active = redis.get(constant.SCHE_AVTIVE_KEY)    # 操作指令 pause暂停调度；resume/start恢复调度
        redis.delete(constant.SCHE_AVTIVE_KEY)          # 操作指令 pause暂停调度；resume/start恢复调度
        try:
            if active:
                if active == constant.ACTIVE_PAUSE and sc.state is STATE_RUNNING:
                    scpprint(f"收到调度指令：{active}，调度服务已暂停")
                    sc.pause()
                elif active == constant.ACTIVE_RESUME:
                    scpprint(f"收到调度指令：{active}，调度服务已恢复")
                    main_event_resume()
                    sc.resume()
                elif sc.state is STATE_STOPPED:
                    scpprint("调度服务已退出【shutdown()】，SchedulerNotRunningError")
                else:
                    scpprint("收到调度指令: %s，但没有做出任何匹配的操作" % active or "None")
            else:
                scpprint("没读取到任务操作指令")
        except Exception as e:
            scpprint("检测到调度服务异常，已关闭；【错误信息】: %s" % str(e))
            sc.shutdown()

if __name__ == '__main__':
    sc.start()
    sc.add_listener(event_callback, EVENT_ALL)      # 无法触发EVENT_SCHEDULER_START
    reload_task(False)
    loop_event()