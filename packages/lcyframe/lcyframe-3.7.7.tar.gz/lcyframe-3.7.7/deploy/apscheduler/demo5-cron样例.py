import datetime
from apscheduler.schedulers.background import BackgroundScheduler


def job1():
	print('job1')


def job2(x, y):
	print('job2', x, y)


scheduler = BackgroundScheduler()
scheduler.start()

# 每天 2 点运行，指定 jobstore 与 executor，默认都为 default
scheduler.add_job(
	job1,
	trigger='cron',
	hour=2,
	jobstore='mem',
	# jobstore="jobstore_name",  # 默认default
	# executor="processpool"  # 默认default，需提前在BackgroundScheduler()中需要配置了executor
)

# 每天 2 点 30 分 5 秒运行
scheduler.add_job(
	job2,
	trigger='cron',
	second=5,
	minute=30,
	hour=2,
	args=['hello', 'world']
)

# 每 10 秒运行一次
scheduler.add_job(
	job1,
	trigger='cron',
	second='*/10'
)

# 匹配字段 a 到 b 之间的取值，a 必须小于 b，包括 a 与 b，比如2-5，则匹配1,2,3,4,5
scheduler.add_job(
	job1,
	trigger='cron',
	minute="1-5"
)

# 匹配 a 到 b 之间每递增 c 后的值，包括 a，不一定包括 b，比如1-20/5，则匹配1,6,11,16
scheduler.add_job(
	job1,
	trigger='cron',
	minute="1-20/5"
)

# 每天 1:00,2:00,3:00 运行
scheduler.add_job(
	job1,
	trigger='cron',
	hour='1-3'
)

# 在 6,7,8,11,12 月的第三个周五 的 1:00,2:00,3:00 运行
scheduler.add_job(
	job1,
	trigger='cron',
	month='6-8,11-12',
	day='3rd fri',
	hour='1-3'
)

# 在 2019-12-31 号之前的周一到周五 5 点 30 分运行
scheduler.add_job(
	job1,
	trigger='cron',
	day_of_week='mon-fri',
	hour=5,
	minute=30,
	end_date='2019-12-31'
)

# 当月的第三个周五
scheduler.add_job(
	job1,
	trigger='cron',
	day_of_week='3rd fri',
)

# 当月的最后一个周五
scheduler.add_job(
	job1,
	trigger='cron',
	day_of_week='last fri',
)