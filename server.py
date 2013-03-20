import tornado.ioloop
import tornado.options

import argparse

from handlers.qr import (CreateQRCodeHandler,
                         GetQRCodeHandler)

application = tornado.web.Application([
    (r"/qrcode", CreateQRCodeHandler),
    (r"/get_qrcode", GetQRCodeHandler),
])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ShareIt API Server")
    parser.add_argument('config_path', metavar='c', type=str, help="Path to config file")
    args = parser.parse_args()
    tornado.options.parse_config_file(args.config_path)

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
