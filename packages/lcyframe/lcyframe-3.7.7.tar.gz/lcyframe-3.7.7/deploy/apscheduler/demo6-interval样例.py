from apscheduler.schedulers.background import BackgroundScheduler


def job():
	print('job')


scheduler = BackgroundScheduler()
scheduler.start()

# 每 2 小时运行一次
scheduler.add_job(
	job,
	trigger='interval',
	hours=2
)

# 2019-10-01 00:00:00 到 2019-10-31 23:59:59 之间每 2 小时运行一次
scheduler.add_job(
	job,
	trigger='interval',
	hours=2,
	start_date='2019-10-01 00:00:00',
	end_date='2019-10-31 23:59:59',
)

# 每 2 天 3 小时 4 分钟 5 秒 运行一次
scheduler.add_job(
	job,
	trigger='interval',
	days=2,
	hours=3,
	minutes=4,
	seconds=5
)