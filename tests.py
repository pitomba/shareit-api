# -*- coding=utf-8 -*-
import unittest, os, os.path, sys, urllib
import tornado.database
import tornado.options
from tornado.options import options
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(APP_ROOT, '..'))

import server

#tornado.options.parse_config_file(os.path.join(APP_ROOT, 'config', 'test.py'))

class TestHandlerBase(AsyncHTTPTestCase):
    def setUp(self):
        super(TestHandlerBase, self).setUp()

    def get_app(self):
        return server.application

    def get_http_port(self):
        return 8888 

    def get_app(self):
        print 'got app!'
        return Application([('/qrcode', server.MainHandler)])

class TestBucketHandler(TestHandlerBase):
    def test_create_qrcode(self):
        get_args = {'msg': 'andreaugusto'}

        print 'here', urllib.urlencode(get_args)

        response = self.http_client.fetch(
                        self.get_url('/qrcode'),
                        self.stop
                        )
        print response

        self.assertEqual(response.code, 200)
'''
def test_homepage(self):
    # The following two lines are equivalent to
    #   response = self.fetch('/')
    # but are shown in full here to demonstrate explicit use
    # of self.stop and self.wait.
    self.http_client.fetch(self.get_url('/'), self.stop)
    response = self.wait()
    # test contents of response
'''
