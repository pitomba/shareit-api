from tornado.web import RequestHandler
from util import qrwrapper
from util import string_generator

import json

import sqlite3

# TODO - Create pooling
# XXX - Search for better place to do this in tornado
def connect_db():
    return sqlite3.connect('shareit.db')

class CreateQRCodeHandler(RequestHandler):

    QRCODE_HEADERS = [
                      ('Content-Type', 'application/json'),
                     ]

    # TODO - Async it!
    def get(self):
        msg = self.get_argument("msg", default=None, strip=False)

        self._apply_headers()
        
        file_name = string_generator.get_new_random_file_name()

        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO images (key, msg) \
                        VALUES (?, ?)', (file_name, msg))
        connection.commit()

        self.write(self.get_json(file_name))

    def get_json(self, file_name):
        response = { 'url': '10.71.11.214:8888/get_qrcode?key=%s' % file_name }
        return "response(%s)" % json.dumps(response)

    # XXX - Dry this
    def _apply_headers(self):
        for header in self.QRCODE_HEADERS:
            self.set_header(*header)


class GetQRCodeHandler(RequestHandler):

    QRCODE_HEADERS = [
                      ('Content-Type', 'image/jpeg'),
                      ('Content-Disposition', 'attachment; filename=qrcode.jpeg'),
                     ]

    def get(self):

        key = self.get_argument("key", default=None, strip=False)

        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("SELECT msg FROM images \
                        WHERE key = :key", {'key':key})

        fetch = cursor.fetchone()

        self._apply_headers()
        
        with open(qrwrapper.get_new_qrcode_path(fetch[0]), 'r') as img:
            self.write(img.read())

    def _apply_headers(self):
        for header in self.QRCODE_HEADERS:
            self.set_header(*header)
