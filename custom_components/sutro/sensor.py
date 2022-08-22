"""Sensor platform for Sutro."""
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor import SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONCENTRATION_PARTS_PER_MILLION
from homeassistant.const import PERCENTAGE
from homeassistant.const import TEMP_FAHRENHEIT
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback


from .const import ATTRIBUTION
from .const import DOMAIN
from .const import ICON_ACIDITY
from .const import ICON_ALKALINITY
from .const import ICON_CHARGES
from .const import ICON_BROMINE
from .const import ICON_CHLORINE
from .const import ICON_HEALTH
from .const import NAME
from .const import VERSION
from .entity import SutroEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Sutro sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            AciditySensor(coordinator, entry),
            AlkalinitySensor(coordinator, entry),
            FreeChlorineSensor(coordinator, entry),
            TemperatureSensor(coordinator, entry),
            BatterySensor(coordinator, entry),
            CartridgeCharges(coordinator, entry),
            BromineSensor(coordinator, entry),
            DeviceHealthSensor(coordinator, entry),
        ]
    )


class SutroSensor(SutroEntity, SensorEntity):
    """sutro Sensor class."""

    _attr_state_class = SensorStateClass.MEASUREMENT

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


class SutroDeviceSensor(SutroSensor):
    """Base class for Sutro Device Sensors."""

    @property
    def extra_state_attributes(self):
        return {
            "reading_time": self.coordinator.data["me"]["pool"]["latestReading"][
                "readingTime"
            ]
        }


class AciditySensor(SutroDeviceSensor):
    """Representation of an Acidity Sensor."""

    _attr_name = f"{NAME} Acidity Sensor"
    _attr_icon = ICON_ACIDITY
    _attr_native_unit_of_measurement = "pH"

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        return float(self.coordinator.data["me"]["pool"]["latestReading"]["ph"])

    @property
    def unique_id(self):
        """Return a unique ID to use for the sensor."""
        return f"{self.coordinator.data['me']['device']['serialNumber']}-acidity"


class AlkalinitySensor(SutroDeviceSensor):
    """Representation of an Alkalinity Sensor."""

    _attr_name = f"{NAME} Alkalinity Sensor"
    _attr_icon = ICON_ALKALINITY
    _attr_native_unit_of_measurement = "mg/L CaC03"

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        return float(self.coordinator.data["me"]["pool"]["latestReading"]["alkalinity"])

    @property
    def unique_id(self):
        """Return a unique ID to use for the sensor."""
        return f"{self.coordinator.data['me']['device']['serialNumber']}-alkalinity"


class FreeChlorineSensor(SutroDeviceSensor):
    """Representation of a Free Chlorine Sensor."""

    _attr_name = f"{NAME} Free Chlorine Sensor"
    _attr_icon = ICON_CHLORINE
    _attr_native_unit_of_measurement = CONCENTRATION_PARTS_PER_MILLION

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        val = self.coordinator.data["me"]["pool"]["latestReading"]["chlorine"]
        if val is None:
            return 0
        return float(val)

    @property
    def unique_id(self):
        """Return a unique ID to use for the sensor."""
        return f"{self.coordinator.data['me']['device']['serialNumber']}-chlorine"


class BromineSensor(SutroDeviceSensor):
    """Representation of a Free Chlorine Sensor."""

    _attr_name = f"{NAME} Bromine Sensor"
    _attr_icon = ICON_BROMINE
    _attr_native_unit_of_measurement = CONCENTRATION_PARTS_PER_MILLION

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        val = self.coordinator.data["me"]["pool"]["latestReading"]["bromine"]
        if val is None:
            return 0
        return float(val)

    @property
    def unique_id(self):
        """Return a unique ID to use for the sensor."""
        return f"{self.coordinator.data['me']['device']['serialNumber']}-bromine"


class TemperatureSensor(SutroSensor):
    """Representation of a Temperature Sensor."""

    _attr_name = f"{NAME} Temperature Sensor"
    _attr_native_unit_of_measurement = TEMP_FAHRENHEIT
    _attr_device_class = SensorDeviceClass.TEMPERATURE

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        return float(self.coordinator.data["me"]["device"]["temperature"])

    @property
    def unique_id(self):
        """Return a unique ID to use for the sensor."""
        return f"{self.coordinator.data['me']['device']['serialNumber']}-temperature"


class BatterySensor(SutroSensor):
    """Representation of a Battery Sensor."""

    _attr_name = f"{NAME} Battery"
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_device_class = SensorDeviceClass.BATTERY

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        return float(self.coordinator.data["me"]["device"]["batteryLevel"])

    @property
    def unique_id(self):
        """Return a unique ID to use for the sensor."""
        return f"{self.coordinator.data['me']['device']['serialNumber']}-battery"


class CartridgeCharges(SutroSensor):
    """Representation of a Cartridge Charges Sensor."""

    _attr_name = f"{NAME} Cartridge Charges"
    _attr_icon = ICON_CHARGES
    _attr_native_unit_of_measurement = "charges"

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        return int(self.coordinator.data["me"]["device"]["cartridgeCharges"])

    @property
    def unique_id(self):
        """Return a unique ID to use for the sensor."""
        return f"{self.coordinator.data['me']['device']['serialNumber']}-charges"


class DeviceHealthSensor(SutroSensor):
    """Representation of a Device Health Sensor."""

    _attr_state_class = None
    _attr_name = f"{NAME} Device Health"
    _attr_icon = ICON_HEALTH
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        return self.coordinator.data["me"]["device"]["health"]

    @property
    def unique_id(self):
        """Return a unique ID to use for the sensor."""
        return f"{self.coordinator.data['me']['device']['serialNumber']}-health"
