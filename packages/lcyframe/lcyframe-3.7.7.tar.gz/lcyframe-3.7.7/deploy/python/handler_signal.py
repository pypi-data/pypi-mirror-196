import signal, logging, tornado
from tornado.httpserver import HTTPServer
from tornado.web import Application
from tornado.ioloop import IOLoop
ioloop = IOLoop.instance()

"""
kill信号处理
"""


def signal_handler(sig, frame):
    ioloop.add_callback(shutdown)


def shutdown():
    logging.warning('Stopping http server')
    http_server.stop()
    ioloop.add_callback(ioloop.stop)

handlers = []
app = Application(handlers)
http_server = HTTPServer(app)
http_server.bind(8080)
signal.signal(signal.SIGINT, signal_handler)        # 相当于kill -2 xxx、Ctrl+C
signal.signal(signal.SIGTERM, signal_handler)       # 想到于kill -15 xxx(等于默认kill xxx)
ioloop.start()
