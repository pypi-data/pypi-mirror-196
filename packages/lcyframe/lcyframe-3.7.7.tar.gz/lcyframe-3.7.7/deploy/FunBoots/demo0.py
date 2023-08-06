"""
设置PYTHONPATH，使得python里能import
export PYTHONPATH="项目的路径"
在没有使用pycahrm运行代码时候，如果实在cmd 或者 linux 运行， python xx.py，
请在临时会话窗口设置linux export PYTHONPATH=你的项目根目录 ，winwdos set PYTHONPATH=你的项目根目录

框架获取配置的方式就是直接import funboost_config，然后将里面的值覆盖框架的 funboost_config_deafult.py 值。
为什么能import 到 funboost_config,是因为要求export PYTHONPATH=你的项目根目录，然后第一次运行时候自动生成配置文件到项目根目录了。

假设你的项目根目录是 /data/app/myproject/

方案一：利用python导入机制，自动import 有PYTHONPATH的文件夹下的配置文件。
   例如你在 /data/config_prod/ 放置 funboost_config.py ,然后shell临时命令行 export PYTHONPATH=/data/config_prod/:/data/app/myproject/,再python xx.py。 （这里export 多个值用：隔开，linux设置环境变量为多个值的基本常识无需多说。）
   这样就能自动优先使用/data/config_prod/里面的funboost_config.py作为配置文件了，因为import自动会优先从这里。
   然后在测试环境 /data/config_test/ 放置 funboost_config.py,然后shell临时命令行 export PYTHONPATH=/data/config_test/:/data/app/myproject/,再python xx.py。
   这样测试环境就能自动使用 /data/config_test/ 里面的funboost_config.py作为配置文件了，因为import自动会优先从这里。

方案二：
   直接在funboost_config.py种写if else，if os.get("env")=="test" REDIS_HOST=xx ，if os.get("env")=="prod" REDIS_HOST=xx ，
   因为配置文件本身就是python文件，所以非常灵活，这不是.ini或者 .yaml文件只能写静态的死字符串和数字，
   python作为配置文件优势本来就很大，里面可以写if else，也可以调用各种函数，只要你的模块下包含那些变量就行了。
"""