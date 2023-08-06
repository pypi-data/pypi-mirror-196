#!/usr/bin/env python
import os, psutil, threading
import sys, json, base64, requests
import uuid
import time

def f():
    while True:
        pid = os.getpid()
        # Mac系统与Linux系统部分信号不一样，linux下-18、-19和mac相反
        print(int(time.time()), f"当前pid：{pid} \n"
                                f"kill -2 pid转后台运行(Mac好像没用，直接被杀死，和-1一样)；\n"
                                f"kill -18 pid暂停运行(Mac)；\n"
                                f"kill -19 pid继续运行(Mac)；")
        with open("1.txt", "a+") as f:
            f.write(str(time.time()) + "\n")
        time.sleep(1)

def run_in_process():
    f()

def run_in_thread():
    for i in range(3):
        threading.Thread(target=f).start()

if __name__ == "__main__":
    # 主进程运行，测试暂停功能
    run_in_process()
    # 线程中运行，测试暂停功能
    # run_in_thread()
