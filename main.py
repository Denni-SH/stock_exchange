from tornado import web, ioloop, options
from tornado.options import parse_command_line, define
import tornado
import os
import handlers

base_dir = os.path.dirname(__file__)
port = 8888

def run_server():
    # constructor
    parse_command_line()
    app =  tornado.web.Application([
        (r"/", handlers.MainHandler),
        (r"/new_order", handlers.AddOrder),
        (r"/status/(?P<pk>\d+)", handlers.MainHandler),
    ],
    debug = True,
            template_path = os.path.join(base_dir, "templates"),
                            static_path = os.path.join(base_dir, "static"),
    )
    app.listen(port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    run_server()
