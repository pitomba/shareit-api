import tornado.ioloop
from tornado.web import RequestHandler
import qrwrapper

class CreateQRCodeHandler(RequestHandler):

    QRCODE_HEADERS = [
                      ('Content-Type', 'image/jpeg'),
                      ('Content-Disposition', 'attachment; filename=qrcode.jpeg'),
                     ]

    def get(self):
        msg = self.get_argument("msg", default=None, strip=False)

        self._apply_headers()
        
        with open(qrwrapper.get_new_qrcode_path(msg), 'r') as img:
            self.write(img.read())

    def _apply_headers(self):
        for header in self.QRCODE_HEADERS:
            self.set_header(*header)
        

application = tornado.web.Application([
    (r"/qrcode", CreateQRCodeHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
