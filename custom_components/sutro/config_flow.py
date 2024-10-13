"""Adds config flow for Sutro."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL
from homeassistant.const import CONF_PASSWORD
from homeassistant.const import CONF_TOKEN
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import SutroLoginApiClient
from .const import DOMAIN


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
