import atexit               # 该模块可以实现，程序退出前进行一些操作，和信号捕获效果类似
import time, loguru

def _at_exit():
    loguru.logger.warning(
        f'程序关闭前，{round(time.time() - 0)} 秒内，累计推送了 publish_msg_num_total 条消息 到 _queue_name 中')


def my_func():
    print("你的业务流程")

    # 退出前收尾工作
    atexit.register(_at_exit)