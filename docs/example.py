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
