EEBrightBox (unstable)
======================

Connector for EE BrightBox routers.

.. image:: https://travis-ci.org/krygal/eebrightbox.svg?branch=master
    :target: https://travis-ci.org/krygal/eebrightbox
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: ./LICENSE
   :alt: MIT licensed

Example
-------

.. code:: python

    from eebrightbox import EEBrightbox

    config = {
        'version': 2,
        'password': 'admin_password'
    }

    with EEBrightbox(config) as ee:
        active_devices = ee.get_active_devices()
        ssids = ee.get_ssids()


License
-------

See LICENSE file
