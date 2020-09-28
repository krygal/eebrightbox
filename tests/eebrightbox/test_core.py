import unittest

from eebrightbox import EEBrightBox
from eebrightbox import EERouter
from eebrightbox import EEBrightBox2
from eebrightbox import EESmartHub


class TestEERouter(unittest.TestCase):

    def test_ee_router_config_deprecated(self):
        self.config = {
            'username': 'admin',
            'password': 'password',
            'host': '192.168.1.1',
            'version': 2
        }

        router = EEBrightBox(self.config)

        self.assertIsInstance(router, EEBrightBox2)

    def test_ee_router_config(self):
        self.config = {
            'username': 'admin',
            'password': 'password',
            'host': '192.168.1.1',
            'version': 2
        }

        router = EERouter(self.config)

        self.assertIsInstance(router, EEBrightBox2)

    def test_ee_router_config_smarthub(self):
        self.config = {
            'host': '192.168.1.1',
            'version': 3
        }

        router = EERouter(self.config)

        self.assertIsInstance(router, EESmartHub)
