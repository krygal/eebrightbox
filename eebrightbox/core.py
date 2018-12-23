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
from .helpers import parse_device_db
from .helpers import parse_ssid_value
from .helpers import parse_to_boolean
from .helpers import parse_to_datetime
from .helpers import parse_to_integer
from .helpers import parse_to_string

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
        Authenticate using username and password.

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
        Perform logout and removes cookies.
        """
        _LOGGER.debug("Logging out")

        endpoint = "http://%s/logout.cgi" % self.host
        requests.post(endpoint, cookies=self.cookies)

        self.cookies = {}

    def get_devices(self):
        """
        Retrieve list of devices (ever) recorded by the router.

        :returns: List of dicts with following keys:
            - mac - XX:XX:XX:XX:XX:XX format
            - hostname
            - port - wl0, wl1, eth0/1/2/3
            - ip - xxx.xxx.xxx.xxx format
            - ipv6
            - ipv6_11
            - time_first_seen - Datetime
            - time_last_active - Datetime
            - activity_ip - True/False
            - activity_ipv6 - True/False
            - activity_ipv6_11 - True/False
            - dhcp_option - likely None
            - name - usually matches hostname or 'Unknown'+mac format
            - os - likely None
            - device - likely None
            - device_oui - likely None
            - device_serial - likely None
            - device_class - likely None
        :raises: AuthenticationException if not authenticated
        """
        devices = self._get_devices()

        _LOGGER.debug('Devices %s', devices)

        return devices

    def get_active_devices(self):
        """
        Retrieve list of active devices connected to router.

        Activity is determined using activity_ip flag.

        :returns: List of dicts with following keys:
            - mac - XX:XX:XX:XX:XX:XX format
            - hostname
            - port - wl0, wl1, eth0/1/2/3
            - ip - xxx.xxx.xxx.xxx format
            - ipv6
            - ipv6_11
            - time_first_seen - Datetime
            - time_last_active - Datetime
            - activity - True/False
            - activity_ip - True/False
            - activity_ipv6 - True/False
            - activity_ipv6_11 - True/False
            - dhcp_option - likely None
            - name - usually matches hostname or 'Unknown'+mac format
            - os - likely None
            - device - likely None
            - device_oui - likely None
            - device_serial - likely None
            - device_class - likely None
        :raises: AuthenticationException if not authenticated
        """
        devices = self._get_devices()
        active_devices = [d for d in devices if d['activity_ip']]

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

        return [s for s in ssids if s['ssid'] is not None]

    def _get_devices(self):
        """
        :returns: List
        """
        _LOGGER.debug("Getting devices")

        # parse XML and retrieve deviceDB node
        root = self._get_status_conn_xml()
        device_db = root.find('deviceDB').get('value')

        # node value is almost-JSON
        devices = parse_device_db(device_db)

        device_configs = [
            ('mac', 'mac', parse_to_string),
            ('hostname', 'hostname', parse_to_string),
            ('port', 'port', parse_to_string),
            ('ip', 'ip', parse_to_string),
            ('ipv6', 'ipv6', parse_to_string),
            ('ipv6_ll', 'ipv6_ll', parse_to_string),
            ('time_first_seen', 'time_first_seen', parse_to_datetime),
            ('time_last_active', 'time_last_active', parse_to_datetime),
            ('activity', 'activity', parse_to_boolean),
            ('activity_ip', 'activity_ip', parse_to_boolean),
            ('activity_ipv6', 'activity_ipv6', parse_to_boolean),
            ('activity_ipv6_ll', 'activity_ipv6_ll', parse_to_boolean),
            ('dhcp_option', 'dhcp_option', parse_to_string),
            ('name', 'name', parse_to_string),
            ('os', 'os', parse_to_string),
            ('device', 'device', parse_to_string),
            ('device_oui', 'device_oui', parse_to_string),
            ('device_serial', 'device_serial', parse_to_string),
            ('device_class', 'device_class', parse_to_string),
        ]

        cleaned_devices = []
        for device in devices:
            clean_device = {}
            for name, friendly_name, convert_function in device_configs:
                clean_device[friendly_name] = convert_function(device[name])
            cleaned_devices.append(clean_device)

        return cleaned_devices

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
