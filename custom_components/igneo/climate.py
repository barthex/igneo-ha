"""Climate platform for Estyma Igneo."""

import logging
from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
)
from homeassistant.const import (
    UnitOfTemperature,
    ATTR_TEMPERATURE,
)
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from . import DOMAIN, IgleoDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up climate entities."""

    coordinator: IgleoDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        IgleoCWUClimate(coordinator, "Hot Water (CWU)"),
        IgleoRoomClimate(coordinator, "Room Temperature"),
    ]

    async_add_entities(entities)


class IgleoBaseClimate(ClimateEntity):
    """Base climate entity for Igleo."""

    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE

    def __init__(self, coordinator: IgleoDataUpdateCoordinator, name: str):
        """Initialize entity."""
        self.coordinator = coordinator
        self._name = name
        self._attr_unique_id = f"{coordinator.device_id}_{name.lower().replace(' ', '_')}"
        self._attr_hvac_modes = [HVACMode.HEAT]
        self._attr_hvac_mode = HVACMode.HEAT

    @property
    def device_info(self):
        """Return device info."""
        return {
            "identifiers": {(DOMAIN, self.coordinator.device_id)},
            "name": "Estyma Igneo Slim",
            "manufacturer": "Estyma",
            "model": "Igneo Slim",
        }

    @property
    def should_poll(self):
        """No polling needed."""
        return False

    @property
    def available(self):
        """Return if entity is available."""
        return self.coordinator.last_update_success

    async def async_added_to_hass(self):
        """Connect to dispatcher."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )


class IgleoCWUClimate(IgleoBaseClimate):
    """CWU (Hot Water) climate entity."""

    @property
    def current_temperature(self):
        """Return current CWU temperature."""
        if self.coordinator.data:
            return self.coordinator.data.cwu_temp
        return None

    @property
    def target_temperature(self):
        """Return target CWU temperature."""
        if self.coordinator.data:
            return self.coordinator.data.cwu_temp_target
        return None

    @property
    def min_temp(self):
        """Return minimum temperature."""
        return 30.0

    @property
    def max_temp(self):
        """Return maximum temperature."""
        return 60.0

    @property
    def target_temperature_step(self):
        """Return temperature step."""
        return 1.0

    async def async_set_temperature(self, **kwargs):
        """Set target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return

        order_number = await self.hass.async_add_executor_job(
            self.coordinator._client.set_cwu_comfort_temp,
            temperature
        )

        if order_number:
            _LOGGER.info("Set CWU temperature to %.1f°C (order #%d)", temperature, order_number)
            # Refresh data
            await self.coordinator.async_refresh()
        else:
            _LOGGER.error("Failed to set CWU temperature")


class IgleoRoomClimate(IgleoBaseClimate):
    """Room temperature climate entity."""

    @property
    def current_temperature(self):
        """Return current room temperature."""
        if self.coordinator.data:
            return self.coordinator.data.room_temp
        return None

    @property
    def target_temperature(self):
        """Return target room temperature (estimated from comfort settings)."""
        # Since we don't have direct target temp, use current + a margin
        if self.coordinator.data:
            return self.coordinator.data.room_temp
        return None

    @property
    def min_temp(self):
        """Return minimum temperature."""
        return 10.0

    @property
    def max_temp(self):
        """Return maximum temperature."""
        return 30.0

    @property
    def target_temperature_step(self):
        """Return temperature step."""
        return 0.5

    async def async_set_temperature(self, **kwargs):
        """Set target room temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return

        order_number = await self.hass.async_add_executor_job(
            self.coordinator._client.set_room_comfort_temp,
            temperature
        )

        if order_number:
            _LOGGER.info("Set room temperature to %.1f°C (order #%d)", temperature, order_number)
            # Refresh data
            await self.coordinator.async_refresh()
        else:
            _LOGGER.error("Failed to set room temperature")
