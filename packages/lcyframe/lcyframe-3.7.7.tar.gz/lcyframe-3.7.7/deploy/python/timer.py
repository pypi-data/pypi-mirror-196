from threading import Timer
from datetime import datetime
 
def printTime(msg):
    print(msg, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

t = Timer(3, printTime, ("线程内挂起", ))
t.start()

print("不阻塞，继续执行")