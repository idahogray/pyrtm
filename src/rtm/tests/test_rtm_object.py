# -*- coding: utf-8 -*-

import os
import sys
from ConfigParser import RawConfigParser
from operator import attrgetter
from os.path import dirname, join as pathjoin, realpath
from nose.plugins.skip import SkipTest
from nose.tools import *
from StringIO import StringIO

import rtm.rtm as RTM

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
        'no_item': '\n\n'
            'rtm.%s.%s: Cannot get response item, maybe there is no item\n',
    }

    def setup(self):
        if not os.access(KEY_TXT, os.R_OK):
            raise SkipTest(self.message['skip'])
        self.read_key_txt()
        self.rtm = RTM.createRTM(self.apikey, self.secret, self.token)

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

    def assert_stat_ok(self, rsp):
        assert_equal(u"ok", rsp.stat)

    def assert_attr(self, methods, rsp):
        for m in methods:
            if type(m) is dict:
                for key in m:
                    assert_true(hasattr(rsp, key))
            else:
                assert_true(hasattr(rsp, m))

    def assert_methods(self, func, **params):
        """high-level assertion for stat/attr of api methods"""
        api, method = func.func_name.replace('test_', '').split('_')
        attr = "%s.%s" % (api, method)
        rsp = attrgetter(attr)(self.rtm)(**params)
        self.assert_stat_ok(rsp)
        rsp_attr = getattr(rsp, api)
        if not isinstance(rsp_attr, RTM.dottedDict):
            raise SkipTest(self.message['no_item'] % (api, method))
        self.assert_attr(RTM.API_RESPONSE[api][method][api], rsp_attr)

    def test_auth_checkToken(self):
        params = {'auth_token': self.token}
        self.assert_methods(self.test_auth_checkToken, **params)

    def test_contacts_getList(self):
        self.assert_methods(self.test_contacts_getList)

    def test_groups_getList(self):
        self.assert_methods(self.test_groups_getList)

    def test_lists_getList(self):
        self.assert_methods(self.test_lists_getList)

    def test_locations_getList(self):
        self.assert_methods(self.test_locations_getList)

    def test_settings_getList(self):
        self.assert_methods(self.test_settings_getList)

    # FIXME: this test is failed
    #def test_tasks_getList(self):
    #    self.assert_methods(self.test_tasks_getList)

    def test_timezones_getList(self):
        self.assert_methods(self.test_timezones_getList)
