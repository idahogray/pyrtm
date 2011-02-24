# -*- coding: utf-8 -*-

import os
import sys
from ConfigParser import RawConfigParser
from os.path import dirname, join as pathjoin, realpath
from nose.plugins.skip import SkipTest
from nose.tools import *
from StringIO import StringIO

import rtm

KEY_TXT = pathjoin(dirname(realpath(__file__)), 'apikey.txt')
KEY_TXT_FORMAT = """
The format are(ConfigParser readable):
[rtm]
apikey: xxx
secret: yyy
token: zzz
"""

class TestRTM(object):

    message = {
        'skip': '\n\n'
            'Set your API key "%s" to run TestRTM for authentication\n'
            '%s' % (KEY_TXT, KEY_TXT_FORMAT),
        'cannot_read': '\n\n'
            'Cannot read "%s"\n'
            '%s' % (KEY_TXT, KEY_TXT_FORMAT),
    }

    def setup(self):
        if not os.access(KEY_TXT, os.R_OK):
            raise SkipTest(self.message['skip'])
        self.read_key_txt()

    def read_key_txt(self):
        try:
            c = RawConfigParser()
            c.read(KEY_TXT)
            self.apikey = c.get('rtm', 'apikey')
            self.secret = c.get('rtm', 'secret')
            self.token = c.get('rtm', 'token')
        except Exception as err:
            print >> sys.stderr, err
            raise SkipTest(self.message['cannot_read'])

    def test_authenticate(self):
        r = rtm.createRTM(self.apikey, self.secret, self.token)
        rsp = r.auth.checkToken(auth_token=self.token)
        assert_equal(u"ok", rsp.stat)
