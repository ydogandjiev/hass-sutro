"""Binary Sensor platform for Sutro."""
from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    DEVICE_CLASS_CONNECTIVITY,
    DEVICE_CLASS_OPENING,
    DEVICE_CLASS_PROBLEM,
)
from homeassistant.helpers.entity import EntityCategory


from .const import ATTRIBUTION
from .const import DOMAIN
from .const import NAME
from .const import VERSION
from .const import ICON_DEVICE_ONLINE
from .entity import SutroEntity


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
    """sutro Binary Sensor class."""

    @property
    def device_info(self):
        """Return the parent device information."""
        device_unique_id = self.coordinator.data["me"]["device"]["serialNumber"]
        return {
            "identifiers": {(DOMAIN, device_unique_id)},
            "name": NAME,
            "model": VERSION,
            "manufacturer": NAME,
        }

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {
            "attribution": ATTRIBUTION,
            "integration": DOMAIN,
        }


class DeviceOnlineBinarySensor(SutroBinarySensor):
    """Representation of an Device Online Binary Sensor."""

    _attr_name = f"{NAME} Device Online"
    _attr_icon = ICON_DEVICE_ONLINE
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def unique_id(self):
        """Return a unique ID to use for the binary sensor."""
        return f"{self.coordinator.data['me']['device']['serialNumber']}-device-online"

    @property
    def device_class(self):
        """Return the class of this binary_sensor."""
        return DEVICE_CLASS_CONNECTIVITY

    @property
    def is_on(self):
        """Return true if the device is connected."""
        return self.coordinator.data["me"]["device"]["online"]


class HubOnlineBinarySensor(SutroBinarySensor):
    """Representation of an Hub Online Binary Sensor."""

    _attr_name = f"{NAME} Hub Online"
    _attr_icon = ICON_DEVICE_ONLINE
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def unique_id(self):
        """Return a unique ID to use for the binary sensor."""
        return f"{self.coordinator.data['me']['device']['serialNumber']}-hub-online"

    @property
    def device_class(self):
        """Return the class of this binary_sensor."""
        return DEVICE_CLASS_CONNECTIVITY

    @property
    def is_on(self):
        """Return true if the device is connected."""
        return self.coordinator.data["me"]["hub"]["online"]


class DeviceLidOpenBinarySensor(SutroBinarySensor):
    """Representation of an Device Online Binary Sensor."""

    _attr_name = f"{NAME} Device Lid Open"

    @property
    def unique_id(self):
        """Return a unique ID to use for the binary sensor."""
        return f"{self.coordinator.data['me']['device']['serialNumber']}-lid-open"

    @property
    def device_class(self):
        """Return the class of this binary_sensor."""
        return DEVICE_CLASS_OPENING

    @property
    def is_on(self):
        """Return true if the binary_sensor is on."""
        return self.coordinator.data["me"]["device"]["lidOpen"]


class CoreStatusBinarySensor(SutroBinarySensor):
    """Representation of an Hub Online Binary Sensor."""

    _attr_name = f"{NAME} Core Status"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def unique_id(self):
        """Return a unique ID to use for the binary sensor."""
        return f"{self.coordinator.data['me']['device']['serialNumber']}-core-status"

    @property
    def device_class(self):
        """Return the class of this binary_sensor."""
        return DEVICE_CLASS_PROBLEM

    @property
    def is_on(self):
        """Return true if the device has a problem."""
        return not self.coordinator.data["me"]["device"]["coreStatus"]


class NotTakingReadingsBinarySensor(SutroBinarySensor):
    """Representation of an Hub Online Binary Sensor."""

    _attr_name = f"{NAME} Taking Readings"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def unique_id(self):
        """Return a unique ID to use for the binary sensor."""
        return f"{self.coordinator.data['me']['device']['serialNumber']}-not-taking-readings"

    @property
    def device_class(self):
        """Return the class of this binary_sensor."""
        return DEVICE_CLASS_PROBLEM

    @property
    def is_on(self):
        """Return true if the device is fine."""
        return not self.coordinator.data["me"]["device"]["shouldTakeReadings"]
