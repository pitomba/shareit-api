#!/usr/bin/env python
import sys
import os

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(APP_ROOT, '..'))

from util import qrwrapper

class TestImageCreator(unittest.TestCase):
    
    def test_image_creation(self):
        TEST_STRING = 'shareit msg'
        qr_path = qrwrapper.get_new_qrcode_path(TEST_STRING)
        self.assertNotEqual(qr_path, None)

if __name__ == '__main__':
    unittest.main()
