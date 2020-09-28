EEBrightBox (unstable)
======================

Connector for EE BrightBox and Smart Hub routers.

.. image:: https://img.shields.io/travis/krygal/eebrightbox/master.svg
    :target: https://travis-ci.org/krygal/eebrightbox
.. image:: https://img.shields.io/librariesio/github/krygal/eebrightbox.svg
.. image:: https://img.shields.io/codeclimate/maintainability-percentage/krygal/eebrightbox.svg
    :target: https://codeclimate.com/github/krygal/eebrightbox
.. image:: https://img.shields.io/codeclimate/coverage/krygal/eebrightbox.svg
    :target: https://codeclimate.com/github/krygal/eebrightbox
.. image:: https://img.shields.io/pypi/v/eebrightbox.svg
    :target: https://pypi.org/project/eebrightbox/
.. image:: https://img.shields.io/pypi/pyversions/eebrightbox.svg
.. image:: https://img.shields.io/pypi/l/eebrightbox.svg


Installation
-------------

 .. code:: bash

    pip install eebrightbox


Example
-------

.. code:: python

    from eebrightbox import EERouter

    config = {
        'version': 2,  # 2 - EE BrightBox 2, 3 - EE Smart Hub
        'host': '192.168.1.1', # optional
        'username': 'admin', # optional
        'password': 'admin_password', # found at the back of the router
    }

    with EERouter(config) as ee:
        active_devices = ee.get_active_devices()

        print(active_devices)
        # Output: [{'mac': '10:AD:E1:2C:68:FE', 'hostname': 'hostname1', 'port': 'wl1', 'ip': '192.168.1.111', 'ipv6': None, 'ipv6_ll': None, 'time_first_seen': datetime.datetime(2018, 12, 9, 14, 46, 28), 'time_last_active': datetime.datetime(2018, 12, 22, 14, 26, 3), 'activity': True, 'activity_ip': True, 'activity_ipv6': False, 'activity_ipv6_ll': True, 'dhcp_option': None, 'name': 'name1', 'os': None, 'device': None, 'device_oui': None, 'device_serial': None, 'device_class': None}, ...]


License
-------

MIT License

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
