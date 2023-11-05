"""Support for Abode Security System switches."""
from __future__ import annotations

from typing import Any, cast

from jaraco.abode.helpers import constants as CONST

from homeassistant.components.switch import SwitchEntity

from .const import DOMAIN

DEVICE_TYPES = [CONST.TYPE_SWITCH, CONST.TYPE_VALVE]

ICON = "mdi:robot"


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Abode switch devices."""
    hub = hass.data[DOMAIN][config_entry.entry_id]

    new_devices = []
    for gorelka in hub.gorelka:
        new_devices.append(GorelkaEnableSwitch(gorelka))
    if new_devices:
        async_add_entities(new_devices)


class GorelkaEnableSwitch(SwitchEntity):
    """Representation of an Abode switch."""

    def __init__(self, gorelka):
        """Initialize the sensor."""
        self._gorelka = gorelka
        self._attr_unique_id = f"{self._gorelka.gorelka_id}_enable"

        # The name of the entity
        self._attr_name = f"{self._gorelka.name} Enable"

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

    def turn_on(self, **kwargs: Any) -> None:
        """Turn on the device."""
        self._gorelka.switch_on()

    def turn_off(self, **kwargs: Any) -> None:
        """Turn off the device."""
        self._gorelka.switch_off()

    @property
    def is_on(self) -> bool:
        """Return true if device is on."""
        return cast(bool, self._gorelka.is_on)
