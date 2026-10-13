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

        errors: Dict[str, str] = {}

        if user_input is not None:
            # Validate credentials
            try:
                import sys
                from pathlib import Path

                src_path = str(Path(__file__).parent.parent.parent / "src")
                if src_path not in sys.path:
                    sys.path.insert(0, src_path)

                from igneo_api import IgleoClient

                client = IgleoClient(
                    user_input[CONF_USERNAME],
                    user_input[CONF_PASSWORD],
                    user_input[CONF_DEVICE_ID],
                )

                if not await self.hass.async_add_executor_job(client.login):
                    errors["base"] = "invalid_auth"
                else:
                    # Check if can fetch data
                    data = await self.hass.async_add_executor_job(
                        client.get_device_data
                    )
                    if not data:
                        errors["base"] = "cannot_connect"
                    else:
                        return self.async_create_entry(
                            title=f"Igneo {user_input[CONF_DEVICE_ID]}",
                            data=user_input,
                        )
            except Exception as err:
                _LOGGER.error("Error during validation: %s", err)
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USERNAME): str,
                    vol.Required(CONF_PASSWORD): str,
                    vol.Required(CONF_DEVICE_ID): str,
                    vol.Optional(CONF_FUEL_CAPACITY, default=75): vol.Range(min=10, max=500),
                    vol.Optional(CONF_DAILY_CONSUMPTION, default=5): vol.Range(min=0.5, max=50),
                    vol.Optional(CONF_LOW_FUEL_THRESHOLD, default=15): vol.Range(min=5, max=50),
                }
            ),
            errors=errors,
            description_placeholders={
                "fuel_info": "Standard fuel load in kg (e.g., 75kg is 5 bags of 15kg each)",
                "consumption_info": "Estimated daily fuel consumption in kg for prediction",
            },
        )
