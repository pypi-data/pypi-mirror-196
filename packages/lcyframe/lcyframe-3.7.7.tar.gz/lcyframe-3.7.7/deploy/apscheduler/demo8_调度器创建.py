"""
配置调度器
APScheduler 提供了多种不同的方式来配置调度器。
假设使用默认 job 存储和默认执行器运行 BackgroundScheduler：
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
以上创建了一个 BackgroundScheduler 调度器，job 存储使用默认的 MemoryJobStore，执行器使用默认的 ThreadPoolExecutor，最大线程数 10 个。

假如想做以下设置：
一个名为 mongo 的 job 存储，后端使用 MongoDB
一个名为 default 的 job 存储，后端使用数据库（使用 Sqlite）
一个名为 default 的线程池执行器，最大线程数 20 个
一个名为 processpool 的进程池执行器，最大进程数 5 个

"""

# 方法一：

from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

jobstores = {
    'mongo': MongoDBJobStore(),
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}

executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}

job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

scheduler = BackgroundScheduler(jobstores=jobstores,
                                executors=executors,
                                job_defaults=job_defaults,
                                # timezone=utc
                                )

# 方法二：
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler({
    'apscheduler.jobstores.mongo': {
         'type': 'mongodb'
    },
    'apscheduler.jobstores.default': {
        'type': 'sqlalchemy',
        'url': 'sqlite:///jobs.sqlite'
    },
    'apscheduler.executors.default': {
        'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
        'max_workers': '20'
    },
    'apscheduler.executors.processpool': {
        'type': 'processpool',
        'max_workers': '5'
    },
    'apscheduler.job_defaults.coalesce': 'false',
    'apscheduler.job_defaults.max_instances': '3',
    'apscheduler.timezone': 'UTC',
})

# 方法三：
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ProcessPoolExecutor

jobstores = {
    'mongo': {'type': 'mongodb'},
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}

executors = {
    'default': {'type': 'threadpool', 'max_workers': 20},
    'processpool': ProcessPoolExecutor(max_workers=5)
}

job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

scheduler = BackgroundScheduler()
scheduler.configure(jobstores=jobstores,
                    executors=executors,
                    job_defaults=job_defaults,
                    # timezone=utc
                    )

# job指定执行器、存储器
scheduler.add_job(
	"test_tick2",
	'interval',
	seconds=5,
	id="0002",
	name="job2",
	args=(7, 8),
	jobstore="mongo",   		# 默认default
	executor="processpool"      # 默认default，需提前在BackgroundScheduler()中需要配置了executor
)