"""
https://funboost.readthedocs.io/zh/latest/articles/c9.html#id3
"""
import asyncio
from funboost import boost, BrokerEnum, ConcurrentModeEnum

@boost("test_queue_1", concurrent_num=ConcurrentModeEnum.ASYNC)
async def f1(x, y):
    await asyncio.sleep(10)
    return x, y

@boost("test_queue_2")
def f2(x, y):
    return x, y

if __name__ == '__main__':
    f1.clear()

    # 生成任务
    for i in range(100):
        f1.push(i, i+1)
        f2.push(i, i+1)

    # 启动1个消费进程
    f1.consume()

    # 启动2个消费进程
    f2.multi_process_consume(2)


    # 远程部署
    f1.fabric_deploy("192.168.10.11", "root", "123456")

    f2.fabric_deploy("192.168.10.11", "root", "123456",
                     sftp_log_level=10,
                     file_volume_limit=100*1000,    # 100k以上的文件不上传
                     only_upload_within_the_last_modify_time=10*24*3600,    # 只上传最近10天修改过的文件
                     process_num=3                  # 一共启动3个进程消费
                     )
