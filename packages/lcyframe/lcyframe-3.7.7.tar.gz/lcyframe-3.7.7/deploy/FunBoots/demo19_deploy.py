"""
程服务器部署函数的意义
框架叫分布式函数调度框架，可以在多台机器运行，因为消息队列任务是共享的。
我用的时候生产环境是使用 阿里云 codepipeline k8s部署的多个容器。还算方便。
在测试环境一般就是单机多进程运行的，用supervisor部署很方便。
所以之前没有涉及到多态机器的轻松自动部署。
如果要实现轻松的部署多台物理机，不借助除了python以外的其他手段的话，只能每台机器登录上然后下载代码，启动运行命令，机器多了还是有点烦的。
现在最新加入了 Python代码级的函数任务部署，不需要借助其他手段，python代码自动上传代码到远程服务器，并自动启动函数消费任务。
目前的自动化在远程机器启动函数消费，连celery都没有做到。

不依赖阿里云codepipeline 和任何运维发布管理工具，只需要在python代码层面就能实现多机器远程部署。
 这实现了函数级别的精确部署，而非是部署一个 .py的代码，远程部署一个函数实现难度比远程部署一个脚本更高一点，部署更灵活。
之前有人问怎么方便的部署在多台机器，一般用阿里云codepipeline  k8s自动部署。被部署的远程机器必须是linux，不能是windwos。
但是有的人是直接操作多台物理机，有些不方便，现在直接加一个利用python代码本身实现的跨机器自动部署并运行函数任务。

自动根据任务函数所在文件，转化成python模块路径，实现函数级别的精确部署，比脚本级别的部署更精确到函数。
例如 test_frame/test_fabric_deploy/test_deploy1.py的fun2函数 自动转化成 from test_frame.test_fabric_deploy.test_deploy1 import f2
从而自动生成部署语句
export PYTHONPATH=/home/ydf/codes/distributed_framework:$PYTHONPATH ;cd /home/ydf/codes/distributed_framework;
python3 -c "from test_frame.test_fabric_deploy.test_deploy1 import f2;f2.multi_process_consume(2)"  -fsdfmark fsdf_fabric_mark_queue_test30

这个是可以直接在远程机器上运行函数任务。无需用户亲自部署代码和启动代码。自动上传代码，自动设置环境变量，自动导入函数，自动运行。
这个原理是使用python -c 实现的精确到函数级别的部署，不是python脚本级别的部署。
可以很灵活的指定在哪台机器运行什么函数，开几个进程。这个比celery更为强大，celery需要登录到每台机器，手动下载代码并部署在多台机器，celery不支持代码自动运行在别的机器上
"""

# export PYTHONPATH=/home/ydf/codes/distributed_framework:$PYTHONPATH ;cd /home/ydf/codes/distributed_framework;python3 -c "from test_frame.test_fabric_deploy.test_deploy1 import f2;f2.multi_process_consume(2)"  -fsdfmark fsdf_fabric_mark_queue_test30
