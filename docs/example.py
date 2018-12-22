from eebrightbox import EEBrightbox

config = {
    'version': 2,
    'password': 'admin_password'
}

with EEBrightbox(config) as ee:
    active_devices = ee.get_active_devices()
    ssids = ee.get_ssids()
