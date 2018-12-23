EEBrightBox (unstable)
======================

Connector for EE BrightBox routers.

.. image:: https://travis-ci.org/krygal/eebrightbox.svg?branch=master
    :target: https://travis-ci.org/krygal/eebrightbox
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: ./LICENSE
   :alt: MIT licensed

Compatibility
-------

 - python 3.6





Example
-------

.. code:: python

    from eebrightbox import EEBrightBox

    config = {
        'version': 2,
        'host': '192.168.1.1', # optional
        'username': 'admin', # optional
        'password': 'admin_password', # found at the back of the router
    }

    with EEBrightBox(config) as ee:
        active_devices = ee.get_active_devices()
        ssids = ee.get_ssids()

        print(active_devices)
        # Output: [{'mac': '34:FC:EF:...', 'hostname': 'android-...', 'ip': '192.168.1.xxx', 'ipv6': '', 'name': 'android-...', 'activity': '1', 'os': 'Unknown', 'device': 'Unknown', 'time_first_seen': '2018/12/01 00:00:00', 'time_last_active': '2018/12/02 00:00:00', 'dhcp_option': 'NA', 'port': 'wl1', 'ipv6_ll': 'fe80::36fc:...', 'activity_ip': '1', 'activity_ipv6_ll': '1', 'activity_ipv6': '0', 'device_oui': 'NA', 'device_serial': 'NA', 'device_class': 'NA'}, ...]

        print(ssids)
        # Output: [{'ssid': 'EE-abcdef', 'enabled': True, 'security': 2, 'password': 'three-word-password', 'broadcast': True}, {'ssid': '5GHz-EE-abcdef', 'enabled': True, 'security': 2, 'password': 'three-word-password', 'broadcast': True}]


License
-------

Copyright (c) 2018 Krystian Galutowski

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
