"""SutroEntity class."""
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION
from .const import DOMAIN
from .const import NAME
from .const import VERSION


class SutroEntity(CoordinatorEntity):
    """Representation of a Sutro Entity."""

    def __init__(self, coordinator, config_entry):
        """Initialize the entity."""
        super().__init__(coordinator)
        self.config_entry = config_entry

    @property
    def device_info(self):
        """Return the parent device information."""
        device_unique_id = self.coordinator.data["me"]["device"]["serialNumber"]
        return {
            "identifiers": {(DOMAIN, device_unique_id)},
            "name": NAME,
            "model": VERSION,
            "manufacturer": NAME,
            "sw_version": self.coordinator.data["me"]["device"][
                "currentFirmwareVersion"
            ],
        }

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {
            "attribution": ATTRIBUTION,
            "integration": DOMAIN,
        }
