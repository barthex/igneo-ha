"""Estyma Igneo Slim integration for Home Assistant."""

import asyncio
import logging
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_USERNAME,
    CONF_PASSWORD,
    Platform,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

DOMAIN = "igneo"
CONF_DEVICE_ID = "device_id"

PLATFORMS = [Platform.SENSOR, Platform.CLIMATE]

SCAN_INTERVAL = timedelta(minutes=5)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Igneo from a config entry."""

    username = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]
    device_id = entry.data[CONF_DEVICE_ID]

    coordinator = IgleoDataUpdateCoordinator(
        hass, username, password, device_id
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, PLATFORMS
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


class IgleoDataUpdateCoordinator(DataUpdateCoordinator):
    """Data update coordinator for Igleo API."""

    def __init__(self, hass: HomeAssistant, username: str, password: str, device_id: str):
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )

        self.username = username
        self.password = password
        self.device_id = device_id
        self._client = None

    async def _async_update_data(self):
        """Fetch data from Igneo API."""
        try:
            # Import here to avoid circular imports
            import sys
            from pathlib import Path

            # Add src to path for igneo_api import
            src_path = str(Path(__file__).parent.parent.parent / "src")
            if src_path not in sys.path:
                sys.path.insert(0, src_path)

            from igneo_api import IgleoClient

            if not self._client:
                self._client = IgleoClient(self.username, self.password, self.device_id)
                await self.hass.async_add_executor_job(self._client.login)

            # Fetch data in executor
            data = await self.hass.async_add_executor_job(
                self._client.get_device_data
            )

            if not data:
                raise UpdateFailed("Failed to fetch device data")

            return data

        except Exception as err:
            _LOGGER.error("Error fetching Igneo data: %s", err)
            raise UpdateFailed(f"Error communicating with API: {err}") from err
