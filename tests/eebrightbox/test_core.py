import os
import unittest

import httpretty

from eebrightbox import AuthenticationException
from eebrightbox import EEBrightBox


class TestEEBrightbox(unittest.TestCase):

    def setUp(self):
        self.config = {
            'username': 'admin',
            'password': 'password',
            'host': '192.168.1.1',
            'version': 2
        }

    def _httpretty_register(self):
        httpretty.register_uri(
            httpretty.POST,
            'http://192.168.1.1/login.cgi',
            body="new_urn = '12345'")

        httpretty.register_uri(
            httpretty.POST,
            'http://192.168.1.1/logout.cgi')

    def _get_response(self, response):
        dir_path = os.path.dirname(os.path.realpath(__file__))

        with open('%s/responses/%s' % (dir_path, response)) as f:
            return f.read()

    def test_defaults(self):
        ee = EEBrightBox({
            'version': 2,
            'password': 'password'
        })
        self.assertEqual(ee.username, 'admin')
        self.assertEqual(ee.host, '192.168.1.1')

    def test_defaults_overwrite(self):
        ee = EEBrightBox({
            'username': 'admin2',
            'password': 'password',
            'host': '192.168.111.1',
            'version': 2
        })
        self.assertEqual(ee.username, 'admin2')
        self.assertEqual(ee.host, '192.168.111.1')

    @httpretty.activate
    def test_authentication(self):
        self._httpretty_register()

        cookies = None
        with EEBrightBox(self.config) as ee:
            cookies = ee.cookies

        self.assertEqual(cookies, {'urn': '12345'})

    @httpretty.activate
    def test_authentication_throws_exception(self):
        httpretty.register_uri(
            httpretty.POST,
            'http://192.168.1.1/login.cgi',
            body="Failed to authenticate")

        cookies = None

        def run():
            with EEBrightBox(self.config) as ee:
                self.assertTrue(False)

        self.assertRaises(AuthenticationException, run)

    @httpretty.activate
    def test_get_active_devices(self):
        self._httpretty_register()

        httpretty.register_uri(
            httpretty.GET,
            'http://192.168.1.1/status_conn.xml',
            body=self._get_response('devices.xml'))

        devices = []
        with EEBrightBox(self.config) as ee:
            devices = ee.get_active_devices()

        self.assertEqual(len(devices), 1)
        self.assertEqual(devices[0]['mac'], '10:AD:E1:2C:68:FE')
        self.assertEqual(devices[0]['ip'], '192.168.1.111')

    @httpretty.activate
    def test_get_ssids(self):
        self._httpretty_register()

        httpretty.register_uri(
            httpretty.GET,
            'http://192.168.1.1/status_conn.xml',
            body=self._get_response('ssids.xml'))

        ssid = []
        with EEBrightBox(self.config) as ee:
            ssid = ee.get_ssids()

        self.assertEqual(len(ssid), 2)
        self.assertEqual(ssid[0]['ssid'], 'EE-abcdef')
        self.assertEqual(ssid[0]['enabled'], True)
        self.assertEqual(ssid[0]['security'], 2)
        self.assertEqual(ssid[0]['password'], 'three-word-password')
        self.assertEqual(ssid[0]['broadcast'], True)

        self.assertEqual(ssid[1]['ssid'], '5GHz-EE-abcdef')
        self.assertEqual(ssid[1]['enabled'], True)
        self.assertEqual(ssid[1]['security'], 2)
        self.assertEqual(ssid[1]['password'], 'three-word-password')
        self.assertEqual(ssid[1]['broadcast'], False)
