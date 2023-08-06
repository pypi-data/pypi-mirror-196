import os, subprocess

# python在shell下执行命令

"""
都是创建子进程运行
"""
# 阻塞，result._proc.pid.可以在命令行下看到输出，ls\ping -c 10 127.0.0.1都不会导致僵尸进程
# result = os.system("ping -c 10 127.0.0.1")

# 非阻塞，result._proc.pid, 可以用read()方法读取输出数据。
# 内部使用subprocess.Popen，ls命令会导致僵尸进程 ping -c 10 127.0.0.1不会
# result = os.popen("ping -c 10 127.0.0.1")
# 命令执行完毕后，打印结果
# stdout = result.readlines()                  # 需等待命令完整执行后

# 非阻塞，且在命令行下输出log。
# result = subprocess.Popen("ls", shell=True)
# redult.pid可以获取子进程pid。
# print(redult.pid)
# ls命令会导致僵尸进程 ping -c 10 127.0.0.1不会

# 如果命令过程，会提示：OSError: [Errno 36] File name too long，解决办法是加上shell=True参数
# result = subprocess.Popen("run_command",
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.PIPE,
#                 shell=True)

# code = result.wait()                                # 添加wait函数，变为阻塞模式，等待子进程结束，防止僵尸进程
# stdout = result.stdout.readlines()                  # 读取命令结果

pass