#!/usr/bin/env python
# -*- coding:utf-8 -*-

from lcyframe import route
from lcyframe import funts
from base import BaseHandler
from tornado.routing import *
@route("/demo")
class DemoHandler(BaseHandler):
    """
    演示使用ap放队列中写入定时任务
    写入成功后，由其他机器的服务执行
    """

    @funts.params()
    def get(self):
        """查看
        测试get

        Request extra query params:
        - a # 角色id type: integer
        - b # 供应商id type: string
        - d # 城市全拼列表 type: int


        :return:
        :rtype:
        """
        # 采用app_start.py方式启动时
        self.application.sc.add_tasks()
        self.write_success({"a": 1})






