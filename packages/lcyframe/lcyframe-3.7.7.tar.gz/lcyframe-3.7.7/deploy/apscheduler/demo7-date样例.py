import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler


def job():
	print('job')

scheduler = BackgroundScheduler()
scheduler.start()

# # 3 秒后运行
# scheduler.add_job(
# 	job,
# 	trigger='date',
# 	run_date=datetime.datetime.now() + datetime.timedelta(seconds=3)
# )
#
# # 2019.11.22 00:00:00 运行
# scheduler.add_job(
# 	job,
# 	trigger='date',
# 	run_date=datetime.date(2019, 11, 22),
# )
#
# # 2019.11.22 16:30:01 运行
# scheduler.add_job(
# 	job,
# 	trigger='date',
# 	run_date=datetime.datetime(2019, 11, 22, 16, 30, 1),
# )
#
# # 2019.11.31 16:30:01 运行
# scheduler.add_job(
# 	job,
# 	trigger='date',
# 	run_date='2019-11-31 16:30:01',
# )

# 立即运行
scheduler.add_job(
	job,
	trigger='date'
)

"""
添加 job 时的日期设置参数 start_date、end_date 以及 run_date都支持字符串格式
1：'2019-12-31' 或者 '2019-12-31 12:01:30'
2：datetime.date（datetime.date(2019, 12, 31)） 
3：datetime.datetime（datetime.datetime(2019, 12, 31, 16, 30, 1)）；
"""