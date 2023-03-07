"""Binary Sensor platform for Sutro."""
import logging
import os

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.binary_sensor import DEVICE_CLASS_CONNECTIVITY
from homeassistant.components.binary_sensor import DEVICE_CLASS_OPENING
from homeassistant.components.binary_sensor import DEVICE_CLASS_PROBLEM
from homeassistant.helpers.entity import EntityCategory

from .const import DOMAIN
from .const import ICON_DEVICE_ONLINE
from .entity import SutroEntity


logger = logging.getLogger(__name__)

NAME = os.environ.get("NAME")


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup binary_sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        [
            DeviceOnlineBinarySensor(coordinator, entry),
            DeviceLidOpenBinarySensor(coordinator, entry),
            HubOnlineBinarySensor(coordinator, entry),
            CoreStatusBinarySensor(coordinator, entry),
            NotTakingReadingsBinarySensor(coordinator, entry),
        ]
    )


class SutroBinarySensor(SutroEntity, BinarySensorEntity):
    """Sutro Binary Sensor class."""


class SutroDeviceBinarySensor(SutroBinarySensor):
    """Base class for Sutro Device Binary Sensors."""

    @property
    def extra_state_attributes(self):
        return {"last_message": self.coordinator.data["me"]["device"]["lastMessage"]}


class SutroHubBinarySensor(SutroBinarySensor):
    """Base class for Sutro Hub Binary Sensors."""

    @property
    def extra_state_attributes(self):
        return {"last_message": self.coordinator.data["me"]["hub"]["lastMessage"]}


class DeviceOnlineBinarySensor(SutroDeviceBinarySensor):
    """Representation of a Device Online Binary Sensor."""

    _attr_name = f"{NAME} Device Online"
    _attr_icon = ICON_DEVICE_ONLINE
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def unique_id(self):
        """Return a unique ID to use for the binary sensor."""
        device_serial = self.coordinator.data["me"]["device"]["serialNumber"]
        return f"{device_serial}-device-online"

    @property
    def device_class(self):
        """Return the class of this binary_sensor."""
        return DEVICE_CLASS_CONNECTIVITY

    @property
    def is_on(self):
        """Return true if the device is connected."""
        return self.coordinator.data["me"]["device"]["online"]


class DeviceLidOpenBinarySensor(SutroDeviceBinarySensor):
    """Representation of a Device Lid Open Binary Sensor."""

    _attr_name = f"{NAME} Device Lid Open"

    @property
    def unique_id(self):
        """Return a unique ID to use for the binary sensor."""
        device_serial = self.coordinator.data["me"]["device"]["serialNumber"]
        return f"{device_serial}-lid-open"

    @property
    def device_class(self):
        """Return the class of this binary_sensor."""
        return DEVICE_CLASS_OPENING

    @property
    def is_on(self):
        """Return true if the binary_sensor is on."""
        return self.coordinator.data["me"]["device"]["lidOpen"]


class CoreStatusBinarySensor(SutroDeviceBinarySensor):
    """Representation of a Core Status Binary Sensor."""

    _attr_name = f"{NAME} Core Status"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def unique_id(self):
        """Return a unique ID to use for the binary sensor."""
        device_serial = self.coordinator.data["me"]["device"]["serialNumber"]
        return f"{device_serial}-core-status"

    @property
    def device_class(self):
        """Return the class of this binary_sensor."""
        return DEVICE_CLASS_PROBLEM

    @property
    def is_on(self):
        """Return true if the device has a problem."""
        return not self.coordinator.data["me"]["device"]["coreStatus"]


class NotTakingReadingsBinarySensor(SutroDeviceBinarySensor):
    """Representation of a Not Taking Readings Binary Sensor."""

    _attr_name = f"{NAME} Taking Readings"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def unique_id(self):
        """Return a unique ID to use for the binary sensor."""
        device_serial = self.coordinator.data["me"]["device"]["serialNumber"]
        return f"{device_serial}-not-taking-readings"

    @property
    def device_class(self):
        """Return the class of this binary_sensor."""
        return DEVICE_CLASS_PROBLEM

    @property
    def is_on(self):
        """Return true if the device is fine."""
        return not self.coordinator.data["me"]["device"]["shouldTakeReadings"]


class HubOnlineBinarySensor(SutroHubBinarySensor):
    """Representation of a Hub Online Binary Sensor."""

    _attr_name = f"{NAME} Hub Online"
    _attr_icon = ICON_DEVICE_ONLINE
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def unique_id(self):
        """Return a unique ID to use for the binary sensor."""
        device_serial = self.coordinator.data["me"]["device"]["serialNumber"]
        return f"{device_serial}-hub-online"

    @property
    def device_class(self):
        """Return the class of this binary_sensor."""
        return DEVICE_CLASS_CONNECTIVITY

    @property
    def is_on(self):
        """Return true if the device is connected."""
        return self.coordinator.data["me"]["hub"]["online"]
