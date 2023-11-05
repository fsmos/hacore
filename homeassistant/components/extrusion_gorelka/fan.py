"""Support for Abode Security System switches."""
from __future__ import annotations

from typing import Any, cast

from homeassistant.components.fan import FanEntity

from .const import DOMAIN

ICON = "mdi:robot"
NIGHTICON = "mdi:weather-night"


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Abode switch devices."""
    hub = hass.data[DOMAIN][config_entry.entry_id]

    new_devices = []
    for gorelka in hub.gorelka:
        new_devices.append(Colorifer1Fan(gorelka))
        new_devices.append(Colorifer2Fan(gorelka))
    if new_devices:
        async_add_entities(new_devices)


class Colorifer1Fan(FanEntity):
    """Representation of an Abode switch."""

    def __init__(self, gorelka):
        """Initialize the sensor."""
        self._gorelka = gorelka
        self._attr_unique_id = f"{self._gorelka.gorelka_id}_fan1"

        # The name of the entity
        self._attr_name = f"{self._gorelka.name} Fan 1"
        self._attr_icon = ICON

    # To link this entity to the cover device, this property must return an
    # identifiers value matching that used in the cover, but no other information such
    # as name. If name is returned, this entity will then also become a device in the
    # HA UI.
    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return {"identifiers": {(DOMAIN, self._gorelka.gorelka_id)}}

    # This property is important to let HA know if this entity is online or not.
    # If an entity is offline (return False), the UI will refelect this.
    @property
    def available(self) -> bool:
        """Return True if roller and hub is available."""
        return self._gorelka.online and self._gorelka.hub.online

    @property
    def percentage(self) -> int | None:
        """Return the current speed."""
        return self._gorelka.fan1_procent

    @property
    def is_on(self) -> bool:
        """Return true if device is on."""
        return cast(bool, self._gorelka.fan1_on)

    async def async_set_percentage(self, percentage: int) -> None:
        """Set the speed of the fan, as a percentage."""
        self._gorelka.set_fan1_procent(percentage)

    async def async_turn_on(
        self,
        percentage: int | None = None,
        preset_mode: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Turn on the entity."""
        self._gorelka.set_fan1_on(percentage)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the entity."""
        self._gorelka.set_fan1_off()


class Colorifer2Fan(FanEntity):
    """Representation of an Abode switch."""

    def __init__(self, gorelka):
        """Initialize the sensor."""
        self._gorelka = gorelka
        self._attr_unique_id = f"{self._gorelka.gorelka_id}_fan2"

        # The name of the entity
        self._attr_name = f"{self._gorelka.name} Fan 2"
        self._attr_icon = NIGHTICON

    # To link this entity to the cover device, this property must return an
    # identifiers value matching that used in the cover, but no other information such
    # as name. If name is returned, this entity will then also become a device in the
    # HA UI.
    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return {"identifiers": {(DOMAIN, self._gorelka.gorelka_id)}}

    # This property is important to let HA know if this entity is online or not.
    # If an entity is offline (return False), the UI will refelect this.
    @property
    def available(self) -> bool:
        """Return True if roller and hub is available."""
        return self._gorelka.online and self._gorelka.hub.online

    @property
    def percentage(self) -> int | None:
        """Return the current speed."""
        return self._gorelka.fan2_procent

    @property
    def is_on(self) -> bool:
        """Return true if device is on."""
        return cast(bool, self._gorelka.fan2_on)

    async def async_set_percentage(self, percentage: int) -> None:
        """Set the speed of the fan, as a percentage."""
        self._gorelka.set_fan2_procent(percentage)

    async def async_turn_on(
        self,
        percentage: int | None = None,
        preset_mode: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Turn on the entity."""
        self._gorelka.set_fan2_on(percentage)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the entity."""
        self._gorelka.set_fan2_off()
