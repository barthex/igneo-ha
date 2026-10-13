"""Services for Estyma Igneo integration."""

import logging
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.service import async_register_admin_service

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

SERVICE_SET_CWU_TEMP = "set_cwu_temperature"
SERVICE_SET_ROOM_TEMP = "set_room_temperature"
SERVICE_INCREASE_TEMP = "increase_temperature"
SERVICE_DECREASE_TEMP = "decrease_temperature"


async def async_setup_services(hass: HomeAssistant) -> None:
    """Register services."""

    async def set_cwu_temperature(call: ServiceCall) -> None:
        """Set CWU (hot water) target temperature."""
        device_id = call.data.get("device_id")
        temperature = call.data.get("temperature")

        if not device_id or temperature is None:
            _LOGGER.error("Missing device_id or temperature")
            return

        coordinator = hass.data[DOMAIN].get(device_id)
        if not coordinator:
            _LOGGER.error(f"Device {device_id} not found")
            return

        order = await hass.async_add_executor_job(
            coordinator._client.set_cwu_comfort_temp,
            temperature
        )

        if order:
            _LOGGER.info(f"Set CWU temp to {temperature}°C (order #{order})")
            await coordinator.async_refresh()
        else:
            _LOGGER.error("Failed to set CWU temperature")

    async def set_room_temperature(call: ServiceCall) -> None:
        """Set room target temperature."""
        device_id = call.data.get("device_id")
        temperature = call.data.get("temperature")

        if not device_id or temperature is None:
            _LOGGER.error("Missing device_id or temperature")
            return

        coordinator = hass.data[DOMAIN].get(device_id)
        if not coordinator:
            _LOGGER.error(f"Device {device_id} not found")
            return

        order = await hass.async_add_executor_job(
            coordinator._client.set_room_comfort_temp,
            temperature
        )

        if order:
            _LOGGER.info(f"Set room temp to {temperature}°C (order #{order})")
            await coordinator.async_refresh()
        else:
            _LOGGER.error("Failed to set room temperature")

    async def increase_temperature(call: ServiceCall) -> None:
        """Increase CWU temperature by 1°C."""
        device_id = call.data.get("device_id")

        coordinator = hass.data[DOMAIN].get(device_id)
        if not coordinator or not coordinator.data:
            _LOGGER.error(f"Device {device_id} not found or no data")
            return

        current = coordinator.data.cwu_temp_target
        new_temp = min(current + 1, 60)

        order = await hass.async_add_executor_job(
            coordinator._client.set_cwu_comfort_temp,
            new_temp
        )

        if order:
            _LOGGER.info(f"Increased CWU temp to {new_temp}°C")
            await coordinator.async_refresh()

    async def decrease_temperature(call: ServiceCall) -> None:
        """Decrease CWU temperature by 1°C."""
        device_id = call.data.get("device_id")

        coordinator = hass.data[DOMAIN].get(device_id)
        if not coordinator or not coordinator.data:
            _LOGGER.error(f"Device {device_id} not found or no data")
            return

        current = coordinator.data.cwu_temp_target
        new_temp = max(current - 1, 30)

        order = await hass.async_add_executor_job(
            coordinator._client.set_cwu_comfort_temp,
            new_temp
        )

        if order:
            _LOGGER.info(f"Decreased CWU temp to {new_temp}°C")
            await coordinator.async_refresh()

    # Register services
    async_register_admin_service(
        hass,
        DOMAIN,
        SERVICE_SET_CWU_TEMP,
        set_cwu_temperature,
        schema={
            "type": "object",
            "properties": {
                "device_id": {"type": "string", "description": "Device ID"},
                "temperature": {"type": "number", "description": "Target temperature (30-60°C)"},
            },
            "required": ["device_id", "temperature"],
        },
    )

    async_register_admin_service(
        hass,
        DOMAIN,
        SERVICE_SET_ROOM_TEMP,
        set_room_temperature,
        schema={
            "type": "object",
            "properties": {
                "device_id": {"type": "string", "description": "Device ID"},
                "temperature": {"type": "number", "description": "Target temperature (10-30°C)"},
            },
            "required": ["device_id", "temperature"],
        },
    )

    async_register_admin_service(
        hass,
        DOMAIN,
        SERVICE_INCREASE_TEMP,
        increase_temperature,
        schema={
            "type": "object",
            "properties": {
                "device_id": {"type": "string", "description": "Device ID"},
            },
            "required": ["device_id"],
        },
    )

    async_register_admin_service(
        hass,
        DOMAIN,
        SERVICE_DECREASE_TEMP,
        decrease_temperature,
        schema={
            "type": "object",
            "properties": {
                "device_id": {"type": "string", "description": "Device ID"},
            },
            "required": ["device_id"],
        },
    )
