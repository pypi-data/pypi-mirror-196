import os, sys, datetime
project_dir = os.path.dirname(__file__)
sys.path.append(os.path.dirname(project_dir))
sys.path.append(project_dir)
import configparser
from publisher import push_for_apscheduler_use_db
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
# redis_jobstore = RedisJobStore()


"""
添加调度任务
"""

class ApSchedulerServer(object):
    def __init__(self, CONFIG):
        self.CONFIG = CONFIG
        self.sc = BackgroundScheduler()
        self.init_server()

    def init_server(self):
        # 存储器
        jobstores = {
            'default': RedisJobStore(
                db=8,
                password=self.CONFIG.get("REDIS", "REDIS_PASSWORD"),
                host=self.CONFIG.get("REDIS", "REDIS_HOST"),
                port=self.CONFIG.get("REDIS", "REDIS_PORT"),
            )
        }
        # 执行器
        executors = {
            'default': ThreadPoolExecutor(20),  # 默认，可以在job中单独指定
            # 'default': {'type': 'threadpool', 'max_workers': 20},
            # 建议尽量使用ProcessPoolExecutor进程池执行器，由于GIL的原因应避免使用线程池
            'processpool': ProcessPoolExecutor(20)   # 可以在job中单独指定processpool执行器
        }
        # GLOBAL VARIABLES
        job_defaults = {
            'coalesce': True,           # 已错过的任务是否合并执行
        }

        self.sc.configure(
            jobstores=jobstores,        # 若将任务放入存储器时，任务函数必须可序列化
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

    def add_tasks(self):
        """
        添加任务
        :return:
        """
        self.sc.add_job(push_for_apscheduler_use_db,
                   'interval', seconds=10, id="wam_id1", name="wam_id1",
                   args=('funboost_tasks.wam', 'engine_wam_task'),
                   kwargs={
                       "task_id": 2,
                       "url": "www.abc.com",
                   },
                   replace_existing=True)

    def modify_task(self):
        """
        更新任务
        :return:
        """

file_path = os.environ.get('PROJECT_CONFIG_FILE')
CONFIG = configparser.ConfigParser()
CONFIG.read(file_path)
ApServer = ApSchedulerServer(CONFIG)

if __name__ == "__main__":
    ApServer.restart_server()