import os, sys
from argparse import ArgumentParser
"""
从命令行获取参数
"""

# 方法一、不指定参数名时，默认按预设参数名排序
def parse_arguments():
    # dp = ' *** use csp scanner'
    # da = "--->   "
    # parser = argparse.ArgumentParser(description=dp, add_help=True)
    # parser.add_argument("base64_data", type=str, default=None, help=f'{da} 包含域名在内的扫描数据字典')
    # parser.add_argument("key", type=str, default=None, help=f'{da} 结果回推的redis key')
    # parser.add_argument("tasks_id", type=str, default=None, help=f'{da} 本次任务的id')
    # parser.add_argument("tasks_name", type=str, default=None, help=f'{da} 本次任务的名称')
    # parser.add_argument("expire", type=str, default=None, help=f'{da} 本次任务的 expire')
    parser = ArgumentParser(description="*** 这是应用的说明 ***", add_help=True)
    parser.add_argument("-c", "--config", dest="config", type=str, default="",
                        help="---> config file path.like ./example.yml")
    parser.add_argument("-p", "--port", dest="port", type=int, default=6677, help="---> the port to run at")
    return parser.parse_args()


args = parse_arguments()
port = args.port        # dest所制定的名称
config = args.config
if not config:
    raise Exception("please run like this：python app.py --config=example.yml")

# shell下调用
# python shell_command_params.py -p 8888 --config = "../example.yml"
# python shell_command_params.py --port 8888 -c = "../example.yml"

# 方法二、不算标准版
for item in sys.argv[1:]:
    arg = item.lstrip("-").lstrip("--")
    if "=" in arg:
        name, equals, value = arg.partition("=")
    else:
        value = arg

    if value.isdigit():
        port = int(value)
        continue
    if ".yml" in value:
        config = value
        continue

if not config:
    raise Exception("please run like this：python app.py --config=example.yml")

# shell下调用
# python shell_command_params.py port=8888 --config=example.yml