import datetime
import os
import unittest

import httpretty

from eebrightbox import EESmartHub


class TestEESmartHub(unittest.TestCase):

    def setUp(self):
        self.config = {
            'host': '192.168.1.1',
        }

    def _get_response(self, response):
        dir_path = os.path.dirname(os.path.realpath(__file__))

        with open('%s/responses/%s' % (dir_path, response)) as f:
            return f.read()

    def test_defaults(self):
        ee = EESmartHub({})
        self.assertEqual(ee.host, '192.168.1.254')

    def test_defaults_overwrite(self):
        ee = EESmartHub({
            'host': '192.168.111.1',
        })
        self.assertEqual(ee.host, '192.168.111.1')

    @httpretty.activate
    def test_get_devices(self):
        httpretty.register_uri(
            httpretty.GET,
            'http://192.168.1.1/cgi/cgi_myNetwork.js',
            body=self._get_response('cgi_myNetwork.js'))

        devices = []
        with EESmartHub(self.config) as ee:
            devices = ee.get_devices()

        expected_device = {
            'mac': '10:AD:E1:2C:68:FE',
            'hostname': 'hostname1',
            'port': 'wl1',
            'ip': '192.168.1.111',
            'ipv6': None,
            'ipv6_ll': None,
            'time_first_seen': datetime.datetime(2018, 12, 9, 14, 46, 28),
            'time_last_active': datetime.datetime(2018, 12, 22, 14, 26, 3),
            'activity': True,
            'activity_ip': True,
            'activity_ipv6': False,
            'activity_ipv6_ll': True,
            'dhcp_option': None,
            'name': 'name1',
            'os': None,
            'device': None,
            'device_oui': None,
            'device_serial': None,
            'device_class': None,
        }

        self.assertEqual([d['mac'] for d in devices], ['10:AD:E1:2C:68:FE', 'AB:72:21:33:11:59', '8A:A4:E4:5B:7B:16', '82:E7:A3:6C:7B:1A', 'F0:8A:76:0A:7C:DA'])
        self.assertEqual(devices[0], expected_device)

    @httpretty.activate
    def test_get_active_devices(self):
        httpretty.register_uri(
            httpretty.GET,
            'http://192.168.1.1/cgi/cgi_myNetwork.js',
            body=self._get_response('cgi_myNetwork.js'))

        devices = []
        with EESmartHub(self.config) as ee:
            devices = ee.get_active_devices()

        self.assertEqual([d['mac'] for d in devices], ['10:AD:E1:2C:68:FE', 'F0:8A:76:0A:7C:DA'])
