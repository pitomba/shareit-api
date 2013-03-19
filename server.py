import tornado.ioloop
import tornado.web
import qrcode

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        msg = self.get_argument("msg", default=None, strip=False)
        image = qrcode.make(msg)
        image.save("qrcode.jpeg")
        self.set_header ('Content-Type', 'image/jpeg')
        self.set_header ('Content-Disposition', 'attachment; filename=qrcode.jpeg')
        with open("qrcode.jpeg", 'r') as img:
            self.write(img.read())

application = tornado.web.Application([
    (r"/qrcode", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
