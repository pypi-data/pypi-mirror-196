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
        # 采用app_start2.py方式启动时
        # from funboost.timing_job.push_fun_for_apscheduler_use_db import push_for_apscheduler_use_db
        from funboost_config import push_for_apscheduler_use_db
        self.application.sc.add_job(push_for_apscheduler_use_db,  # 这个可以定时调用push_for_apscheduler_use_db，需要把文件路径和函数名字传来。
              'interval', seconds=10, id="wam_id1", name="wam_id1",
              args=('funboost_events.wam', 'engine_wam_request'), kwargs={"url": "www.abc.com"},
              replace_existing=True)
        self.write_success({"a": 1})






