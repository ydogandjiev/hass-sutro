"""Sensor platform for Sutro."""
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor import SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONCENTRATION_PARTS_PER_MILLION
from homeassistant.const import PERCENTAGE
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .const import ICON_ACIDITY
from .const import ICON_ALKALINITY
from .const import ICON_BROMINE
from .const import ICON_CHARGER
from .const import ICON_CHARGES
from .const import ICON_CHLORINE
from .const import ICON_HEALTH
from .const import ICON_RECOMMENDATION
from .const import ICON_WIFI
from .const import NAME
from .entity import SutroEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the sensors for the Sutro integration."""
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
            HubChargerStatusSensor(coordinator, entry),
            HubWifiSSIDSensor(coordinator, entry),
            RecommendationSensor(coordinator, entry),
        ]
    )


class SutroSensor(SutroEntity, SensorEntity):
    """sutro Sensor class."""

    _attr_state_class = SensorStateClass.MEASUREMENT


class SutroDeviceSensor(SutroSensor):
    """Base class for Sutro Device Sensors."""

    @property
    def extra_state_attributes(self):
        """Return a dictionary containing the last message."""
        return {"last_message": self.coordinator.data["me"]["device"]["lastMessage"]}


class SutroDeviceReadingSensor(SutroDeviceSensor):
    """Base class for Sutro Device Reading Sensors."""

    @property
    def extra_state_attributes(self):
        """Return a dictionary containing the latest reading."""
        return super().extra_state_attributes | {
            "reading_time": self.coordinator.data["me"]["pool"]["latestReading"][
                "readingTime"
            ],
        }


class SutroHubSensor(SutroSensor):
    """Base class for Sutro Hub Sensors."""

    @property
    def extra_state_attributes(self):
        """Return a dictionary containing the last message."""
        return {"last_message": self.coordinator.data["me"]["hub"]["lastMessage"]}


class AciditySensor(SutroDeviceReadingSensor):
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


class AlkalinitySensor(SutroDeviceReadingSensor):
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


class FreeChlorineSensor(SutroDeviceReadingSensor):
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


class BromineSensor(SutroDeviceReadingSensor):
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


class TemperatureSensor(SutroDeviceSensor):
    """Representation of a Temperature Sensor."""

    _attr_name = f"{NAME} Temperature Sensor"
    _attr_native_unit_of_measurement = UnitOfTemperature.FAHRENHEIT
    _attr_device_class = SensorDeviceClass.TEMPERATURE

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        return float(self.coordinator.data["me"]["device"]["temperature"])

    @property
    def unique_id(self):
        """Return a unique ID to use for the sensor."""
        return f"{self.coordinator.data['me']['device']['serialNumber']}-temperature"


class BatterySensor(SutroDeviceSensor):
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


class CartridgeCharges(SutroDeviceSensor):
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


class DeviceHealthSensor(SutroDeviceSensor):
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


class HubChargerStatusSensor(SutroHubSensor):
    """Representation of a Device Health Sensor."""

    _attr_state_class = None
    _attr_name = f"{NAME} Hub Charger Status"
    _attr_icon = ICON_CHARGER
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        return self.coordinator.data["me"]["hub"]["chargerStatus"]

    @property
    def unique_id(self):
        """Return a unique ID to use for the sensor."""
        return f"{self.coordinator.data['me']['device']['serialNumber']}-charger-status"


class HubWifiSSIDSensor(SutroHubSensor):
    """Representation of a Device Health Sensor."""

    _attr_state_class = None
    _attr_name = f"{NAME} Hub Wi-Fi SSID"
    _attr_icon = ICON_WIFI
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        return self.coordinator.data["me"]["hub"]["ssid"]

    @property
    def unique_id(self):
        """Return a unique ID to use for the sensor."""
        return f"{self.coordinator.data['me']['device']['serialNumber']}-hub-ssid"


class RecommendationSensor(SutroHubSensor):
    """Representation of a Recommendation Sensor."""

    _attr_state_class = None
    _attr_name = f"{NAME} Recommendation"
    _attr_icon = ICON_RECOMMENDATION

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        return self.coordinator.data["me"]["pool"]["latestRecommendations"]["recommendations"][0]["treatment"]

    @property
    def unique_id(self):
        """Return a unique ID to use for the sensor."""
        return f"{self.coordinator.data['me']['device']['serialNumber']}-recommendation"
