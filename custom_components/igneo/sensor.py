"""Sensor platform for Estyma Igneo."""

import logging
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import (
    UnitOfTemperature,
    UnitOfEnergy,
    UnitOfMass,
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
    """Set up sensors."""

    coordinator: IgleoDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = [
        IgleoBoilerTemperatureSensor(coordinator, "Boiler Temperature"),
        IgleoBoilerCalculatedTemperatureSensor(coordinator, "Boiler Calculated Temperature"),
        IgleoRoomTemperatureSensor(coordinator, "Room Temperature"),
        IgleoCWUTemperatureSensor(coordinator, "CWU Temperature"),
        IgleoCWUTargetTemperatureSensor(coordinator, "CWU Target Temperature"),
        IgleoFuelCounterSensor(coordinator, "Fuel Counter"),
        IgleoOxygenLevelSensor(coordinator, "Oxygen Level"),
        IgleoBurnerStatusSensor(coordinator, "Burner Status"),
    ]

    async_add_entities(sensors)


class IgleoBaseSensor(SensorEntity):
    """Base class for Igleo sensors."""

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


class IgleoBoilerTemperatureSensor(IgleoBaseSensor):
    """Boiler temperature sensor."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    @property
    def native_value(self):
        """Return boiler temperature."""
        if self.coordinator.data:
            return self.coordinator.data.boiler_temp
        return None


class IgleoBoilerCalculatedTemperatureSensor(IgleoBaseSensor):
    """Boiler calculated temperature sensor."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    @property
    def native_value(self):
        """Return boiler calculated temperature."""
        if self.coordinator.data:
            return self.coordinator.data.boiler_temp_calculated
        return None


class IgleoRoomTemperatureSensor(IgleoBaseSensor):
    """Room temperature sensor."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    @property
    def native_value(self):
        """Return room temperature."""
        if self.coordinator.data:
            return self.coordinator.data.room_temp
        return None


class IgleoCWUTemperatureSensor(IgleoBaseSensor):
    """CWU (hot water) temperature sensor."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    @property
    def native_value(self):
        """Return CWU temperature."""
        if self.coordinator.data:
            return self.coordinator.data.cwu_temp
        return None


class IgleoCWUTargetTemperatureSensor(IgleoBaseSensor):
    """CWU target temperature sensor."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    @property
    def native_value(self):
        """Return CWU target temperature."""
        if self.coordinator.data:
            return self.coordinator.data.cwu_temp_target
        return None


class IgleoFuelCounterSensor(IgleoBaseSensor):
    """Fuel counter sensor."""

    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_native_unit_of_measurement = UnitOfMass.KILOGRAMS

    @property
    def native_value(self):
        """Return fuel counter."""
        if self.coordinator.data:
            return self.coordinator.data.fuel_counter
        return None


class IgleoOxygenLevelSensor(IgleoBaseSensor):
    """Oxygen level in exhaust sensor."""

    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "%"

    @property
    def native_value(self):
        """Return oxygen level."""
        if self.coordinator.data:
            return self.coordinator.data.oxygen_level
        return None


class IgleoBurnerStatusSensor(IgleoBaseSensor):
    """Burner status sensor."""

    @property
    def native_value(self):
        """Return burner status."""
        if self.coordinator.data:
            return self.coordinator.data.burner_status
        return None
