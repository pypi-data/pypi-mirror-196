from start import app
import datetime
import pytz

@app.task
def add3(x):
    pass

# 延时执行1，在指定时间执行
# eta2utc = datetime.datetime.now() + datetime.timedelta(seconds=10)
# add3.apply_async(kwargs={"x": 99999}, eta=eta2utc.astimezone(pytz.utc).replace(tzinfo=None))
# # 延迟执行2：下次执行时间为60s后。celery会转为eta值（utc格式）放入队列
# add3.apply_async(kwargs={"x": 12}, countdown=60)

# 任务过期：任务触发执行时判断，该任务是否设置了过期时间expires。若过期则废弃；否则执行。
eta2utc = datetime.datetime.now() + datetime.timedelta(seconds=15)
# 指定utc时间
expires_at = (datetime.datetime.now() + datetime.timedelta(seconds=10)).astimezone(pytz.utc).replace(tzinfo=None)
# 指定秒数
# expires_at = 60
add3.apply_async(kwargs={"x": 60},
                 # eta=eta2utc.astimezone(pytz.utc).replace(tzinfo=None),
                 # expires=expires_at
                 )