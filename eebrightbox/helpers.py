"""
Helpers.
"""

import re
import urllib.parse


def parse_to_string(val):
    """
    Convert value to string.
    """
    return str(val)


def parse_to_integer(val):
    """
    Convert value to integer.
    """
    return int(val)


def parse_to_boolean(val):
    """
    Convert value to boolean.
    """
    return val in [True, 'True', 'true', 1, '1', 'Yes', 'yes']


def parse_device_db(device_db):
    """
    Parse device_db structure to list of dicts.
    """
    device_re = r"{([^}]*)}"
    prop_re = r"(\w+):'([^']*)'"
    devices = []

    device_items = re.findall(device_re, device_db)

    for device_item in device_items:
        props = re.findall(prop_re, device_item)

        device = {}
        for prop in props:
            device[prop[0]] = urllib.parse.unquote(prop[1])

        devices.append(device)

    return devices


def parse_ssid_value(ssid_value):
    """
    Parse ssid value to a list.
    """
    val_re = r"'([^']*)'"
    ssid = []

    ssid_items = re.findall(val_re, ssid_value)

    for ssid_item in ssid_items:
        ssid.append(urllib.parse.unquote(ssid_item))

    return ssid
