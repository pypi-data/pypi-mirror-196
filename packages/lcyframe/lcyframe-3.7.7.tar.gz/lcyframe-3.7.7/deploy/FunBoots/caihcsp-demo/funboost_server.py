import os, sys, signal, time
import traceback, logging, psutil
project_dir = os.path.dirname(__file__)
sys.path.append(os.path.dirname(project_dir))
sys.path.append(project_dir)
from argparse import ArgumentParser
from scheduler.common.base import redis
from scheduler.funboost_tasks import wam, system, spider, demo, task, html
from common import constant, wam_mixin, main_mixin
from scheduler.common import utils
def parse_arguments():
    parser = ArgumentParser(description="调取引擎消费端服务", add_help=True)
    parser.add_argument("-c", "--consume", dest="consume", type=str, default="",
                        help="消费者名称:启动进程数(默认1)。多个消费者用逗号','隔开, 例：-c main:5,wam:1,spider,html")
    return parser.parse_args()

try:
    args = parse_arguments()
    utils.fbpprint(f"解析参数:{args.consume}")
    consume_str = args.consume.replace(" ", "")
    if consume_str:
        args_list = args.consume.split(",")
    else:
        args_list = ["main:1", "wam:1", "spider:1", "html:1"]

    for index, item in enumerate(args_list):
        args_list[index] = item.replace(" ", "").split(":")
except Exception as e:
    print(traceback.format_exc(limit=20))
    utils.fbpprint("解析参数错误，启动失败")
    exit()


"""
消费服务：每一个func作为模版，负责消费同一种类型（表）的任务
"""
pid = os.getpid()
def signal_handler(sig, frame):
    utils.fbpprint(f"检测到退出信号sig：{sig},")
    process = psutil.Process(pid)
    for child in process.children():
        print(f"子进程/消费者退出: {child.pid}")
        child.kill()
    print(f"主进程退出: {pid}")
    process.kill()
    sys.exit()
    # os._exit(-1)  # status：4444

if __name__ == '__main__':
    utils.fbpprint("开始运行...")
    # 清除未退出的消费子进程
    utils.clear_childconsume()
    for name, num in args_list:
        try:
            num = int(num)
            # 可用性监测
            if name == "wam":
                # 将所有正处于运行中的任务状态改为失败（因超时、重启、被杀死等原因无法修正的异常任务）
                wam_mixin.revise_task_status()
                wam.engine_wam_task.multi_process_consume(num)
                # wam.engine_wam_task.wait_for_possible_has_finish_all_tasks(10)    # 判断队列所有任务是否消费完成了
            # 任务监测
            elif name == "main":
                main_mixin.revise_task_status()
                task.engine_main_task.multi_process_consume(num)
            # go爬虫
            if name == "spider":
                # 确保爬虫并发数量不少于任务main并发数，防止没有爬虫消费者执行，导致排队超10分钟未抓取回数据被杀死
                # go.num >= main.num
                spider.go_spider_task.multi_process_consume(num)
            elif name == "html":
                # 处理html的并发数>=爬虫并发数*10~15倍（爬虫爬虫爬虫抓取10个页面所花费的时间内，只能成功处理1个html。）
                html.handler_html_task.multi_process_consume(num)

            if name in ["wam", "main"]:
                # 自重启supervisor server
                system.restart_server.multi_process_consume()

                # 消费启动，通知调度系统恢复运行
                p = redis.pipeline()
                p.lpush(constant.SCHE_LISTEN_KEY, 1)
                p.set(constant.SCHE_AVTIVE_KEY, constant.ACTIVE_RESUME)
                p.execute()
        except Exception as e:
            logging.error(traceback.format_exc())
            exit()

    # 一次性运行所有消费者
    # for queue_name, f in boost_queue__fun_map.items():
    #     f.consume()

    # demo.consume_func.clear()
    # demo.consume_func.consume()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    while True: time.sleep(100)