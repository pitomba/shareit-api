from tornado.web import RequestHandler
from util import qrwrapper
from util import apply_headers
from util.string_generator import get_new_random_file_name

import json
import base64

import sqlite3

# XXX - Change to correct domain
DEFAULT_HEADERS = [
                    ('Access-Control-Allow-Origin', '*'),
                  ]

class BaseHandler(RequestHandler):

    def initialize(self, db_connection):
        self.db_connection = db_connection


class CreateQRCodeHandler(BaseHandler):

    RESPONSE_HEADERS = [
                        ('Content-Type', 'application/json'),
                       ]

    RESPONSE_HEADERS += DEFAULT_HEADERS

    MSG_PARAM_NAME = 'msg'

    # TODO - Async it!
    def get(self):

        apply_headers(self, self.RESPONSE_HEADERS + DEFAULT_HEADERS)

        msg = self.get_argument(self.MSG_PARAM_NAME, default=None, strip=False)
        file_name = get_new_random_file_name()
        self._start_msg_processing(file_name, msg)

        self.write(self._get_json(file_name))


    def _get_json(self, file_name):
        # XXX - Change this!
        URL = '10.71.11.214:8888/get_qrcode?key=%s' % file_name

        response = { 'url': URL }
        return json.dumps(response)


    # TODO - Put msg into a msg queue to be processed
    # Solution now is a prototype
    def _start_msg_processing(self, file_name, msg):
        SQL = 'INSERT INTO images (key, msg) \
               VALUES (?, ?)'

        cursor = self.db_connection.cursor()
        cursor.execute(SQL, (file_name, msg))
        self.db_connection.commit()


class GetQRCodeHandler(BaseHandler):

    RAW_RESPONSE_HEADERS = [
                             ('Content-Type', 'image/jpeg'),
                             ('Content-Disposition', 'attachment; filename=qrcode.jpeg'),
                           ]
    
    BASE64_RESPONSE_HEADERS = [
                                ('Content-Type', 'text/plain'),
                              ]

    KEY_PARAM_NAME = 'key'


    def get(self, type):

        key = self.get_argument(self.KEY_PARAM_NAME, default=None, strip=False)
        msg = self._get_msg_from_key(key)
        
        if type == 'raw':
            apply_headers(self, DEFAULT_HEADERS + self.RAW_RESPONSE_HEADERS)
            self._return_raw_file(msg)
        elif type == 'base64':
            apply_headers(self, DEFAULT_HEADERS + self.BASE64_RESPONSE_HEADERS)
            self._return_base64(msg)
        else:
            print 'ops'
            self.send_error(404)


    def _return_raw_file(self, msg):
        with open(qrwrapper.get_new_qrcode_path(msg), 'r') as img:
            self.write(img.read())


    def _return_base64(self, msg):
        with open(qrwrapper.get_new_qrcode_path(msg), 'r') as img:
            coded = base64.b64encode(img.read())
            self.write(coded)
        

    def _get_msg_from_key(self, key):

        SQL = "SELECT msg FROM images \
               WHERE key = :key"

        MSG_INDEX = 0

        cursor = self.db_connection.cursor()
        cursor.execute(SQL, {'key':key})
        
        fetch = cursor.fetchone()[MSG_INDEX]
