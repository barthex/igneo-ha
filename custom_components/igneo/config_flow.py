"""Config flow for Estyma Igneo integration."""

import logging
from typing import Any, Dict

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.data_entry_flow import FlowResult

from . import DOMAIN, CONF_DEVICE_ID

CONF_FUEL_CAPACITY = "fuel_capacity"
CONF_DAILY_CONSUMPTION = "daily_consumption"
CONF_LOW_FUEL_THRESHOLD = "low_fuel_threshold"

_LOGGER = logging.getLogger(__name__)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle config flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: Dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle user initiated flow."""

        if user_input is not None:
            return self.async_create_entry(
                title=f"Igneo {user_input[CONF_DEVICE_ID]}",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USERNAME): str,
                    vol.Required(CONF_PASSWORD): str,
                    vol.Required(CONF_DEVICE_ID): str,
                    vol.Optional(CONF_FUEL_CAPACITY, default=75): int,
                    vol.Optional(CONF_DAILY_CONSUMPTION, default=5): int,
                    vol.Optional(CONF_LOW_FUEL_THRESHOLD, default=15): int,
                }
            ),
        )
