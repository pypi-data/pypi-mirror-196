from funboost.function_result_web.app import app
from flask import render_template, Flask, request, url_for, jsonify, flash, redirect
"""

web代码在funboost包里面，所以可以直接使用命令行运行起来，不需要用户现亲自下载代码就可以直接运行。

4.11 开启消费状态、结果web页面
（1）需要安装mongodb，并且设置 MONGO_URL 的值;安装pymongo3.13.0版本：
 pip install pymongo==3.13.0

如果需要使用这个页面，那么无论选择何种中间件，即使不是使用mongo作为消息队列，也需要安装mongodb，因为因为是从这里读取数据的。
需要在 funboost_config.py 中设置MONGO_URL的值，mongo url的格式如下，这是通用的可以百度mongo url连接形式。
有密码 MONGO_CONNECT_URL = f'mongodb://yourname:yourpassword@127.0.01:27017/admin'
没密码 MONGO_CONNECT_URL = f'mongodb://192.168.6.132:27017/'

（2） 装饰器上需要设置持久化的配置参数,代码例子
框架默认不会保存消息状态和结果到mongo的，因为大部分人并没有安装mongo，且这个web显示并不是框架代码运行的必须部分，还有会降低一丝丝运行性能。
框架插入mongo的原理是采用先进的自动批量聚合插入，例如1秒运行几千次函数，并不会操作几千次mongo，是2秒操作一次mongo
如果需要页面显示消费状态和结果，需要配置装饰器的 function_result_status_persistance_conf 的参数
FunctionResultStatusPersistanceConfig的如参是 (is_save_status: bool, is_save_result: bool, expire_seconds: int)
is_save_status 指的是是否保存消费状态，这个只有设置为True,才会保存消费状态到mongodb，从而使web页面能显示该队列任务的消费信息
is_save_result 指的是是否保存消费结果，如果函数的结果超大字符串或者对函数结果不关心或者函数没有返回值，可以设置为False。
expire_seconds 指的是多久以后，这些保存的数据自动从mongodb里面消失删除，避免爆磁盘。

from funboost import boost, FunctionResultStatusPersistanceConfig
@boost('queue_test_f01', qps=2, function_result_status_persistance_conf=FunctionResultStatusPersistanceConfig(True, True, 7 * 24 * 3600))
def f(a, b):
    return a + b
    
（3） 启动python分布式函数调度框架之函数运行结果状态web
# 第一步 export PYTHONPATH=你的项目根目录 ，这么做是为了这个web可以读取到你项目根目录下的funboost_config.py里面的配置
# 例如 export PYTHONPATH=/home/ydf/codes/ydfhome
  或者  export PYTHONPATH=./   (./是相对路径，前提是已近cd到你的项目根目录了)

第二步   
win上这么做 python3 -m funboost.function_result_web.app 

linux上可以这么做使用gunicorn启动性能好一些，当然也可以按win的做。
gunicorn -w 4 --threads=30 --bind 0.0.0.0:27018 funboost.function_result_web.app:app

（4）使用浏览器打开 http://127.0.0.1:27018
输入默认用户名:admin 密码:123456
"""

app.jinja_env.auto_reload = True
with app.test_request_context():
    print(url_for('query_cols_view'))

app.run(debug=True, threaded=True, host='0.0.0.0', port=27018)
