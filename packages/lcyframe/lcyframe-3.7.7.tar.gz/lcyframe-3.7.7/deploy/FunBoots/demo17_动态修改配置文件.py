"""
这个问题是问一个项目中，有些脚本要连接192.168.0.1的redis ，有些脚本要连接192.168.0.2的redis，但框架配置文件只有一个，如何解决？
例如目录结构是
your_proj /
    funboost_config.py(此文件是第一次启动任意消费脚本后自动生成的，用户按需修改配置)
    dira / a_consumer.py(此脚本中启动funa函数消费)
    dirb / b_consumer.py(此脚本中启动funb函数消费）

如果funa函数要连接192.168.0.1的redis，funb函数要连接192.168.0.2的redis，
有两种解决方式
第一种是在启动消费的脚本，脚本里面手动调用patch_frame_config()函数来设置各种中间件的值
第二种是把funboost_config.py分别复制到dira和dirb文件夹.这种就会自动优先使用a_consumer.py和b_consumer.py同文件夹层级的配置了，
而非是自动优先读取python项目根目录的配置文件，这个是利用了python语言的import模块导入优先级机制。
"""