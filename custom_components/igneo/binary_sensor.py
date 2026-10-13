"""Binary sensor platform for Estyma Igneo."""

import logging
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
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
    """Set up binary sensors."""

    coordinator: IgleoDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = [
        IgleoLowFuelSensor(coordinator, "Low Fuel Alert"),
        IgleoBurnerRunning(coordinator, "Burner Active"),
        IgleoHighBoilerTempSensor(coordinator, "High Boiler Temperature"),
    ]

    async_add_entities(sensors)


class IgleoBaseBinarySensor(BinarySensorEntity):
    """Base class for binary sensors."""

    def __init__(self, coordinator: IgleoDataUpdateCoordinator, name: str):
        """Initialize sensor."""
        self.coordinator = coordinator
        self._name = name
        self._attr_unique_id = f"{coordinator.device_id}_{name.lower().replace(' ', '_')}"

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


class IgleoLowFuelSensor(IgleoBaseBinarySensor):
    """Low fuel alert sensor (alert when < 50kg)."""

    _attr_device_class = BinarySensorDeviceClass.PROBLEM

    @property
    def is_on(self):
        """Return True if fuel is low."""
        if self.coordinator.data:
            # Alert if less than 50kg
            return self.coordinator.data.fuel_counter < 50000
        return False


class IgleoBurnerRunning(IgleoBaseBinarySensor):
    """Burner running/heating sensor."""

    _attr_device_class = BinarySensorDeviceClass.RUNNING

    @property
    def is_on(self):
        """Return True if burner is heating."""
        if self.coordinator.data:
            # Active when status is "grzanie" (heating)
            return self.coordinator.data.burner_status == "grzanie"
        return False


class IgleoHighBoilerTempSensor(IgleoBaseBinarySensor):
    """High boiler temperature alert (> 80°C)."""

    _attr_device_class = BinarySensorDeviceClass.PROBLEM

    @property
    def is_on(self):
        """Return True if boiler temp is high."""
        if self.coordinator.data:
            return self.coordinator.data.boiler_temp > 80
        return False
