"""Constants for Sutro."""
from homeassistant.const import Platform

# Base component constants
NAME = "Sutro"
DOMAIN = "sutro"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.1"

ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"
ISSUE_URL = "https://github.com/ydogandjiev/hass-sutro/issues"

# Icons
ICON_ACIDITY = "mdi:ph"
ICON_ALKALINITY = "mdi:test-tube"
ICON_BROMINE = "mdi:water-percent"
ICON_CHARGER = "mdi:battery-charging"
ICON_CHLORINE = "mdi:water-percent"
ICON_BATTERY = "mdi:battery"
ICON_CHARGES = "mdi:water-outline"
ICON_DEVICE_ONLINE = "mdi:check-network-outline"
ICON_HEALTH = "mdi:hospital-box"
ICON_RECOMMENDATION = "mdi:format-list-checks"
ICON_WIFI = "mdi:wifi"

# Platforms
PLATFORMS = [Platform.SENSOR, Platform.BINARY_SENSOR, Platform.TODO]

# Configuration and options
CONF_TOKEN = "token"

# Logging
STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here: {ISSUE_URL}
-------------------------------------------------------------------
"""
