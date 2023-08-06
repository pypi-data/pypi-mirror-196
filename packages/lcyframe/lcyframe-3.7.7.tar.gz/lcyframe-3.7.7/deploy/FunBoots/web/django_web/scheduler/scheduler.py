# -*- coding: utf-8 -*-
import os, sys, datetime, json, time, uuid
project_dir = os.path.dirname(__file__)
sys.path.append(os.path.dirname(project_dir))
sys.path.append(project_dir)
import configparser
from publisher import push_for_apscheduler_use_db
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
# redis_jobstore = RedisJobStore()


"""
添加调度任务
"""


class MyCronTrigger(CronTrigger):
    @classmethod
    def my_from_crontab(cls, expr, timezone=None):
        values = expr.split()
        if len(values) == 7:
            return cls(second=values[0], minute=values[1], hour=values[2], day=values[3], month=values[4],
                       day_of_week=values[5], year=values[6], timezone=timezone)
        elif len(values) == 5:
            return CronTrigger.from_crontab(expr)
        else:
            raise ValueError('cron表达式错误，支持格式：[分时日月周]、[秒分时日月周年]')

class ApSchedulerServer(object):
    def __init__(self, CONFIG):
        self.CONFIG = CONFIG
        self.sc = BackgroundScheduler()
        self.redis_jobstore = RedisJobStore(
                db=8,
                password=self.CONFIG.get("REDIS", "REDIS_PASSWORD"),
                host=self.CONFIG.get("REDIS", "REDIS_HOST"),
                port=self.CONFIG.get("REDIS", "REDIS_PORT"),
            )
        self.redis8 = self.redis_jobstore.redis
        self.redis7 = RedisJobStore(
                db=7,
                password=self.CONFIG.get("REDIS", "REDIS_PASSWORD"),
                host=self.CONFIG.get("REDIS", "REDIS_HOST"),
                port=self.CONFIG.get("REDIS", "REDIS_PORT"),
            ).redis
        self.init_server()

    def init_server(self):
        jobstores = {
            'default': self.redis_jobstore
        }
        executors = {
            'default': ThreadPoolExecutor(20),
            'processpool': ProcessPoolExecutor(20)
        }
        # GLOBAL VARIABLES
        job_defaults = {
            'coalesce': True,           # 已错过的任务是否合并执行
        }

        self.sc.configure(
            jobstores=jobstores,
            executors=executors,
            job_defaults=job_defaults,
        )
        self.sc.start(paused=True)

    def restart_server(self):
        """
        重启
        :return:
        """
        self.sc.add_job(push_for_apscheduler_use_db,
                   'date',
                   run_date=datetime.datetime.now() + datetime.timedelta(seconds=10),
                   id="restart_server", name="restart_server",
                   args=('funboost_tasks.system', 'restart_server'),
                   kwargs={
                       "server_name": "funboost"
                   },
                   replace_existing=True)

    def add_wam_task(self, task):
        """
        添加可用性任务
        """
        self.__add_tasks(str(task.id),
                       "可用性:" + task.taskname or "任务名未定义",
                       task.assets_cronjob,
                       'funboost_tasks.wam',
                       'engine_wam_task',
                       replace_existing=True,
                       **{"task_id": task.id, "url": task.url})

    def add_main_task(self, task):
        """
        添加检测任务
        """
        self.__add_tasks(str(task.id),
                       "任务监控:" + task.taskname or "任务名未定义",
                       task.assets_cronjob,
                       'funboost_tasks.task',
                       'engine_main_task',
                       replace_existing=True,
                       **{"task_id": task.id})

    def start_wam_task(self, task):
        """
        开始\启用可用性任务
        """
        self.__push_xadd("engine_wam_task", task_id=str(task.id), url=task.url)

    def start_main_task(self, task):
        """
        开始\启用监测任务
        """
        self.__push_xadd("engine_main_task", task_id=str(task.id))

    def stop_main_task(self, task):
        """
        停止\禁用任务
        """
        self.redis7.setex(f"TaskStop:{task.id}", 3600, 1)

    def modify_main_task(self, task):
        """
        编辑任务
        """
        self.add_main_task(task)
        self.start_main_task(task)

    def __add_tasks(self, id, name, crontab_str, func_filename, func_name, replace_existing=True, **kwargs):
        """
        添加任务
        :return:
        """
        self.sc.add_job(push_for_apscheduler_use_db,
                        MyCronTrigger.my_from_crontab(crontab_str),
                        id=str(id), name=name,
                        args=(func_filename, func_name),
                        kwargs=kwargs,
                        replace_existing=replace_existing)

    def __push_xadd(self, queue_name, **kwargs):
        now = time.time()
        kwargs["task_at"] = now
        kwargs["extra"] = {"task_id": f"{queue_name}_result:{uuid.uuid1()}",
                           "publish_time": now,
                           "publish_time_format": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                           }
        self.redis8.xadd(queue_name, {"": json.dumps(kwargs)})


if __name__ == "__main__":
    import os
    import sys
    import logging
    import django
    current_dir = os.path.dirname(__file__)
    sys.path.append(current_dir)
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Server.settings")
    django.setup()
    file_path = os.environ.get('ENGINE_ENV_FILE')
    CONFIG = configparser.ConfigParser()
    CONFIG.read(file_path)

    from saas import models
    ApServer = ApSchedulerServer(CONFIG)
    # ApServer.add_wam_task(models.WAMTasks.objects.get(id=2))
    # ApServer.start_wam_task(models.WAMTasks.objects.get(id=2))
    # ApServer.stop_main_task(models.WAMTasks.objects.get(id=2))