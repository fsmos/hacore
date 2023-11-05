"""A demonstration 'hub' that connects several devices."""
from __future__ import annotations

# In a real implementation, this would be in an external library that's on PyPI.
# The PyPI package needs to be included in the `requirements` section of manifest.json
# See https://developers.home-assistant.io/docs/creating_integration_manifest
# for more information.
# This dummy hub always returns 3 rollers.
import asyncio
from collections.abc import Callable
import random

from homeassistant.core import HomeAssistant


class Hub:
    """Dummy hub for Hello World example."""

    manufacturer = "ExtrusIon"

    def __init__(self, hass: HomeAssistant, host: str, name: str) -> None:
        """Init dummy hub."""
        self._host = host
        self._hass = hass
        self._name = name
        self._id = host.lower()
        self.gorelka = [
            Gorelka(f"{self._id}_1", f"{self._name} 1", self),
        ]
        self.online = True

    @property
    def hub_id(self) -> str:
        """ID for dummy hub."""
        return self._id

    async def test_connection(self) -> bool:
        """Test connectivity to the Dummy hub is OK."""
        await asyncio.sleep(1)
        return True


class Gorelka:
    """Dummy roller (device for HA) for Hello World example."""

    def __init__(self, gorelkaid: str, name: str, hub: Hub) -> None:
        """Init dummy roller."""
        self._id = gorelkaid
        self.hub = hub
        self.name = name
        self._callbacks: set[Callable[[], None]] = set()
        self._loop = asyncio.get_event_loop()
        self._set_temp_main = 20
        self._temp_main = 20
        self._temp_ext = 20
        self._temp_disel = 20
        self._temp_oil = 20
        self._is_on = False
        self._fire = 1000
        self._is_night_mode = False
        self._is_alarm = False
        self._fan1_procent = 0
        self._fan1_on = False
        self._fan2_procent = 0
        self._fan2_on = False
        self._main_status = "work"

        # Some static information about this device
        self.firmware_version = f"0.0.{random.randint(1, 9)}"
        self.model = "Gorelka"

    @property
    def gorelka_id(self) -> str:
        """Return ID for roller."""
        return self._id

    @property
    def position(self):
        """Return position for roller."""
        return self._current_position

    async def set_temp_cotel(self, temp: int) -> None:
        """Set dummy cover to the given position.

        State is announced a random number of seconds later.
        """
        self._set_temp_main = temp

        self._loop.create_task(self.delayed_update())

    def switch_on(self) -> None:
        """Set dummy cover to the given position.

        State is announced a random number of seconds later.
        """
        self._is_on = True

        self._loop.create_task(self.delayed_update())

    def switch_off(self) -> None:
        """Set dummy cover to the given position.

        State is announced a random number of seconds later.
        """
        self._is_on = False

        self._loop.create_task(self.delayed_update())

    def switch_night_mode_on(self) -> None:
        """Set dummy cover to the given position.

        State is announced a random number of seconds later.
        """
        self._is_night_mode = True

        self._loop.create_task(self.delayed_update())

    def switch_night_mode_off(self) -> None:
        """Set dummy cover to the given position.

        State is announced a random number of seconds later.
        """
        self._is_night_mode = False

        self._loop.create_task(self.delayed_update())

    def set_fan1_procent(self, procent) -> None:
        """Set dummy cover to the given position.

        State is announced a random number of seconds later.
        """
        self._fan1_procent = procent

        self._loop.create_task(self.delayed_update())

    def set_fan1_on(self, procent) -> None:
        """Set dummy cover to the given position.

        State is announced a random number of seconds later.
        """
        self._fan1_procent = procent
        self._fan1_on = True
        self._loop.create_task(self.delayed_update())

    def set_fan1_off(self) -> None:
        """Set dummy cover to the given position.

        State is announced a random number of seconds later.
        """
        self._fan1_on = False

        self._loop.create_task(self.delayed_update())

    def set_fan2_procent(self, procent) -> None:
        """Set dummy cover to the given position.

        State is announced a random number of seconds later.
        """
        self._fan2_procent = procent

        self._loop.create_task(self.delayed_update())

    def set_fan2_on(self, procent) -> None:
        """Set dummy cover to the given position.

        State is announced a random number of seconds later.
        """
        self._fan2_procent = procent
        self._fan2_on = True
        self._loop.create_task(self.delayed_update())

    def set_fan2_off(self) -> None:
        """Set dummy cover to the given position.

        State is announced a random number of seconds later.
        """
        self._fan2_on = False

        self._loop.create_task(self.delayed_update())

    async def delayed_update(self) -> None:
        """Publish updates, with a random delay to emulate interaction with device."""
        await asyncio.sleep(random.randint(1, 10))
        await self.publish_updates()

    def register_callback(self, callback: Callable[[], None]) -> None:
        """Register callback, called when Roller changes state."""
        self._callbacks.add(callback)

    def remove_callback(self, callback: Callable[[], None]) -> None:
        """Remove previously registered callback."""
        self._callbacks.discard(callback)

    # In a real implementation, this library would call it's call backs when it was
    # notified of any state changeds for the relevant device.
    async def publish_updates(self) -> None:
        """Schedule call all registered callbacks."""

        for callback in self._callbacks:
            callback()

    @property
    def online(self) -> float:
        """Roller is online."""
        # The dummy roller is offline about 10% of the time. Returns True if online,
        # False if offline.
        return True

    @property
    def temp_main(self) -> int:
        """Main temp."""
        return self._temp_main

    @property
    def temp_ext(self) -> int:
        """Ext temp."""
        return self._temp_ext

    @property
    def temp_disel(self) -> int:
        """Disel temp ."""
        return self._temp_disel

    @property
    def temp_oil(self) -> int:
        """Oil Temp."""
        return self._temp_oil

    @property
    def fire(self) -> int:
        """Oil Temp."""
        return self._fire

    @property
    def is_on(self) -> bool:
        """Oil Temp."""
        return self._is_on

    @property
    def is_night_mode(self) -> bool:
        """Oil Temp."""
        return self._is_night_mode

    @property
    def is_alarm(self) -> bool:
        """Oil Temp."""
        return self._is_alarm

    @property
    def fan1_procent(self) -> int:
        """Fan 1."""
        return self._fan1_procent

    @property
    def fan2_procent(self) -> int:
        """Fan 2."""
        return self._fan2_procent

    @property
    def fan1_on(self) -> bool:
        """Fan 1."""
        return self._fan1_on

    @property
    def fan2_on(self) -> bool:
        """Fan 2."""
        return self._fan2_on

    @property
    def main_status(self) -> str:
        """Fan 2."""
        return self._main_status
