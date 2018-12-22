"""
Support for EE Brightbox 2 router
"""

import hashlib
import logging
import re
import xml.etree.ElementTree as ET

import requests

from .errors import AuthenticationException
from .errors import EEBrightBoxException
from .helpers import parse_to_boolean
from .helpers import parse_to_integer
from .helpers import parse_to_string
from .helpers import parse_device_db
from .helpers import parse_ssid_value

_LOGGER = logging.getLogger(__name__)


class EEBrightBox:
    """EE Brightbox 2 router connector."""

    def __init__(self, config):
        """Initialise the router connector."""
        config_defaults = {'host': '192.168.1.1', 'username': 'admin'}
        config = {**config_defaults, **config}

        self.version = int(config['version'])
        self.host = config['host']
        self.username = config['username']
        self.password_hash = hashlib.md5(config['password'].encode('utf-8')).hexdigest()

        self.cookies = {}

        if self.version not in [2]:
            raise EEBrightBoxException('Unsupported version %s. Only version 2 is currently supported' % self.version)

    def __enter__(self):
        if not self.authenticate():
            raise AuthenticationException('Failed to authenticate')

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.forget()

        return exc_type is None

    def authenticate(self):
        """
        Authenticates using username and password.

        :returns: True/False
        """
        _LOGGER.debug("Authenticating %s", self.username)

        endpoint = "http://%s/login.cgi" % self.host
        response = requests.post(
            endpoint,
            cookies=self.cookies,
            data={
                'usr': self.username,
                'pws': self.password_hash,
                'GO': 'status.htm',
            })

        urn_re = r"new_urn\ \=\ '(.*)'"
        matches = re.search(urn_re, response.text)

        if matches is None:
            _LOGGER.error("Authentication failed %s", response.text)
            return False

        urn = matches.group(1)
        self.cookies = dict(urn=urn)
        _LOGGER.debug("Authenticated with cookie %s", urn)
        return True

    def is_authenticated(self):
        """
        Check if successfully completed authentication.

        :returns: True/False
        """
        return 'urn' in self.cookies

    def forget(self):
        """
        Performs logout and removes cookies.
        """
        _LOGGER.debug("Logging out")

        endpoint = "http://%s/logout.cgi" % self.host
        requests.post(endpoint, cookies=self.cookies)

        self.cookies = {}

    def get_active_devices(self):
        """
        Retrieves list of active devices connected to router.

        Activity is determined using activity_ip flag.

        :returns: List of dicts with following keys:
            - mac
            - hostname
            - ip
            - ipv6
            - name - usually matches hostname or 'Unknown'+mac format
            - os - likely 'Unknown'
            - device - likely 'Unknown'
            - time_first_seen - YYYY/MM/DD HH:mm:ss
            - time_last_active - YYYY/MM/DD HH:mm:ss
            - dhcp_option - likely NA
            - port - wl0, wl1, eth0/1/2/3
            - ipv6_11
            - activity_ip - 0/1
            - activity_ipv6_11 - 0/1
            - activity_ipv6 - 0/1
            - device_oui - likely NA
            - device_serial - likely NA
            - device_class - likely NA
        :raises: AuthenticationException if not authenticated
        """
        devices = self._get_devices()
        active_devices = [d for d in devices if 'activity_ip' in d and str(d['activity_ip']) == '1']

        _LOGGER.debug('Active devices %s', active_devices)

        return active_devices

    def get_ssids(self):
        """
        :returns: List of dicts with following keys:
            - ssid
            - enabled - True/False
            - security - int
            - password
            - broadcast - True/False
        """
        _LOGGER.debug("Getting ssid")

        # parse XML and retrieve deviceDB node
        root = self._get_status_conn_xml()

        node_configs = [
            ('ssid_ssid', 'ssid', parse_to_string),
            ('ssid_ssidEnable', 'enabled', parse_to_boolean),
            ('ssid_security', 'security', parse_to_integer),
            ('ssid_wpaPassword', 'password', parse_to_string),
            ('ssid_broadcast', 'broadcast', parse_to_boolean),
        ]

        ssids = []
        for node_name, friendly_name, convert_function in node_configs:
            node_value = parse_ssid_value(root.find(node_name).get('value'))
            for index, entry in enumerate(node_value):
                try:
                    ssids[index][friendly_name] = convert_function(entry)
                except IndexError:
                    ssids.append({friendly_name: convert_function(entry)})

        return [s for s in ssids if s['ssid'] != '']

    def _get_status_conn_xml(self):
        """
        :returns: ElementTree or None
        """
        if not self.is_authenticated():
            raise AuthenticationException('Not authenticated')

        endpoint = "http://%s/status_conn.xml" % self.host
        try:
            response = requests.get(endpoint, cookies=self.cookies)
            _LOGGER.debug("Response %s", response.text)

            return ET.fromstring(response.text)
        except requests.RequestException:
            _LOGGER.error("Status failed %s", endpoint, exc_info=1)

        return None

    def _get_devices(self):
        """
        :returns: List
        """
        _LOGGER.debug("Getting devices")

        # parse XML and retrieve deviceDB node
        root = self._get_status_conn_xml()
        device_db = root.find('deviceDB').get('value')

        # node value is almost-JSON
        return parse_device_db(device_db)
