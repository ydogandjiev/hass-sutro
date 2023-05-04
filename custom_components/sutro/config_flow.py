"""Adds config flow for Sutro."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry
from homeassistant.config_entries import OptionsFlow
from homeassistant.const import CONF_EMAIL
from homeassistant.const import CONF_PASSWORD
from homeassistant.const import CONF_TOKEN
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import SutroLoginApiClient
from .const import DOMAIN
from .const import PLATFORMS


class SutroFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for sutro."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._password: str | None = None
        self._email: str | None = None
        self._errors = {}

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            data = await self._get_login_data(
                email=user_input[CONF_EMAIL], password=user_input[CONF_PASSWORD]
            )
            stored_data = {}
            if data and "login" in data and data["login"] is not None:
                stored_data[CONF_TOKEN] = data["login"]["token"]

                pool_type = "Pool/Spa"
                if data["login"]["user"]["pool"]["type"]:
                    pool_type = data["login"]["user"]["pool"]["type"].title()
                return self.async_create_entry(
                    title=f"{data['login']['user']['firstName']}'s {pool_type}",
                    data=stored_data,
                )

            self._errors["base"] = "auth"
            return await self._show_config_form(user_input)

        return await self._show_config_form(user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        """Get options flow for configuring Sutro."""
        return SutroOptionsFlowHandler(config_entry)

    async def _show_config_form(self, user_input):  # pylint: disable=unused-argument
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_EMAIL): str,
                    vol.Required(CONF_PASSWORD): str,
                }
            ),
            errors=self._errors,
        )

    async def _get_login_data(self, email: str, password: str) -> dict | None:
        """Return the token if can login."""
        try:
            session = async_create_clientsession(self.hass)
            client = SutroLoginApiClient(session)
            return await client.async_get_login(email, password)
        except Exception as ex:
            self.hass.components.logger.error(f"Failed to get login data: {ex}")
        return None


class SutroOptionsFlowHandler(config_entries.OptionsFlow):
    """Config flow options handler for sutro."""

    def __init__(self, config_entry):
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(
        self, user_input=None
    ) -> FlowResult:  # pylint: disable=unused-argument
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(x, default=self.options.get(x, True)): bool
                    for x in sorted(PLATFORMS)
                }
            ),
        )

    async def _update_options(self):
        """Update config entry options."""
        return self.async_create_entry(
            title=self.config_entry.data.get(CONF_TOKEN), data=self.options
        )
