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
