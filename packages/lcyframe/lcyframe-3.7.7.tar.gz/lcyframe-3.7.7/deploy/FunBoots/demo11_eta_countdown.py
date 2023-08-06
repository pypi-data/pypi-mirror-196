# 需要用publish，而不是push，这个前面已经说明了，如果要传函数入参本身以外的参数到中间件，需要用publish。
# 不然框架分不清哪些是函数入参，哪些是控制参数。如果无法理解就，就好好想想琢磨下celery的 apply_async 和 delay的关系。

from test_frame.test_delay_task.test_delay_consume import f
import datetime
import time
from funboost import PriorityConsumingControlConfig

"""
延迟执行

因为有很多人有这样的需求，希望发布后不是马上运行，而是延迟60秒或者现在发布晚上18点运行。
然来是希望用户自己亲自在消费函数内部写个sleep(60)秒再执行业务逻辑，来达到延时执行的目的，
但这样会被sleep占据大量的并发线程/协程,如果是用户消费函数内部写sleep7200秒这么长的时间，那
sleep等待会占据99.9%的并发工作线程/协程的时间，导致真正的执行函数的速度大幅度下降，所以框架
现在从框架层面新增这个延时任务的功能。

之前已做的功能是定时任务，现在新增延时任务，这两个概念有一些不同。

定时任务一般情况下是配置为周期重复性任务，延时任务是一次性任务。
1）框架实现定时任务原理是代码本身自动定时发布，自然而然就能达到定时消费的目的。
2）框架实现延时任务的原理是马上立即发布，当消费者取出消息后，并不是立刻去运行，
   而是使用定时运行一次的方式延迟这个任务的运行。

在需求开发过程中，我们经常会遇到一些类似下面的场景：
1）外卖订单超过15分钟未支付，自动取消
2）使用抢票软件订到车票后，1小时内未支付，自动取消
3）待处理申请超时1天，通知审核人员经理，超时2天通知审核人员总监
4）客户预定自如房子后，24小时内未支付，房源自动释放


分布式函数调度框架的延时任务概念类似celery的countdown和eta入参，  add.apply_async(args=(1, 2),countdown=20)  # 规定取出后20秒再运行
此框架的入参名称那就也叫 countdown和eta。
countdown 传一个数字，表示多少秒后运行。
eta传一个datetime对象表示，精确的运行时间运行一次。

测试发布延时任务，不是发布后马上就执行函数。

countdown 和 eta 只能设置一个。
countdown 指的是 离发布多少秒后执行，
eta是指定的精确时间运行一次。

misfire_grace_time 是指定消息轮到被消费时候，如果已经超过了应该运行的时间多少秒之内，仍然执行。
misfire_grace_time 如果设置为None，则消息一定会被运行，不会由于大连消息积压导致消费时候已近太晚了而取消运行。
misfire_grace_time 如果不为None，必须是大于等于1的整数，此值表示消息轮到消费时候超过本应该运行的时间的多少秒内仍然执行。
此值的数字设置越小，如果由于消费慢的原因，就有越大概率导致消息被丢弃不运行。如果此值设置为1亿，则几乎不会导致放弃运行(1亿的作用接近于None了)
如果还是不懂这个值的作用，可以百度 apscheduler 包的 misfire_grace_time 概念

"""
for i in range(1, 20):
    time.sleep(1)

    # 消息发布10秒后再执行。如果消费慢导致任务积压，misfire_grace_time为None，即使轮到消息消费时候离发布超过10秒了仍然执行。
    f.publish({'x': i}, priority_control_config=PriorityConsumingControlConfig(countdown=10))

    # 规定消息在17点56分30秒运行，如果消费慢导致任务积压，misfire_grace_time为None，即使轮到消息消费时候已经过了17点56分30秒仍然执行。
    f.publish({'x': i * 10}, priority_control_config=PriorityConsumingControlConfig(
        eta=datetime.datetime(2021, 5, 19, 17, 56, 30) + datetime.timedelta(seconds=i)))

    # 消息发布10秒后再执行。如果消费慢导致任务积压，misfire_grace_time为30，如果轮到消息消费时候离发布超过40 (10+30) 秒了则放弃执行，
    # 如果轮到消息消费时候离发布时间是20秒，由于 20 < (10 + 30)，则仍然执行
    f.publish({'x': i * 100}, priority_control_config=PriorityConsumingControlConfig(
        countdown=10, misfire_grace_time=30))

    # 规定消息在17点56分30秒运行，如果消费慢导致任务积压，如果轮到消息消费时候已经过了17点57分00秒，
    # misfire_grace_time为30，如果轮到消息消费时候超过了17点57分0秒 则放弃执行，
    # 如果如果轮到消息消费时候是17点56分50秒则执行。
    f.publish({'x': i * 1000}, priority_control_config=PriorityConsumingControlConfig(
        eta=datetime.datetime(2021, 5, 19, 17, 56, 30) + datetime.timedelta(seconds=i),
        misfire_grace_time=30))

    # 这个设置了消息由于推挤导致运行的时候比本应该运行的时间如果小于1亿秒，就仍然会被执行，所以几乎肯定不会被放弃运行
    f.publish({'x': i * 10000}, priority_control_config=PriorityConsumingControlConfig(
        eta=datetime.datetime(2021, 5, 19, 17, 56, 30) + datetime.timedelta(seconds=i),
        misfire_grace_time=100000000))