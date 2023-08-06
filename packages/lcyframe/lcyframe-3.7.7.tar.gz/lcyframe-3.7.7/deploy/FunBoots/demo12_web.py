"""在web中如flask fastapi django 如何搭配使用消费框架的例子。
在web中推送任务，后台进程消费任务，很多人问怎么在web使用，用法和不与web框架搭配并没有什么不同之处。


因为发布和消费是使用中间件解耦的，一般可以分成web接口启动一次，后台消费启动一次，需要独立部署两次。

演示了flask 使用app应用上下文。

web接口中发布任务到消息队列，独立启动异步消费。
flask + 分布式函数调度框架演示例子在：

https://github.com/ydf0509/distributed_framework/blob/master/test_frame/use_in_flask_tonardo_fastapi

fastapi + 分布式函数调度框架演示例子在：

https://github.com/ydf0509/fastapi_use_distributed_framework_demo

django + 分布式函数调度框架演示例子在：

https://github.com/ydf0509/django_use_funboost

这三个web框架demo + funboost 框架，几乎是一模一样的，有的人不能举一反三，非要我单独增加demo例子。

部署方式都是web部署一次，后台消费部署一次，web接口中发布消息到消息队列，funboost没有与任何框架有任何绑定关系，都是一样的用法。

如果前端在乎任务的结果：

非常适合使用mqtt， 前端订阅唯一uuid的topic 然后表单中带上这个topic名字请求python接口 -> 接口中发布任务到rabbitmq或redis消息队列 ->
后台消费进程执行任务消费,并将结果发布到mqtt的那个唯一uuid的topic -> mqtt 把结果推送到前端。
使用ajax轮训或者后台导入websocket相关的包来做和前端的长耗时任务的交互 是伪命题。"""

from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

# 任务
from .func import create_report

# django.user.views.py
def test(request):
    create_report.push('hello')
    return HttpResponse("发布消息成功")