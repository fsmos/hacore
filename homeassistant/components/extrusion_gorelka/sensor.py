"""Platform for sensor integration."""
# This file shows the setup for the sensors associated with the cover.
# They are setup in the same way with the call to the async_setup_entry function
# via HA from the module __init__. Each sensor has a device_class, this tells HA how
# to display it in the UI (for know types). The unit_of_measurement property tells HA
# what the unit is, so it can display the correct range. For predefined types (such as
# battery), the unit_of_measurement should match what's expected.

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import UnitOfTemperature
from homeassistant.helpers.entity import Entity

from .const import DOMAIN

FIREICON = "mdi:fire"


# See cover.py for more details.
# Note how both entities for each roller sensor (battry and illuminance) are added at
# the same time to the same list. This way only a single async_add_devices call is
# required.
async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    hub = hass.data[DOMAIN][config_entry.entry_id]

    new_devices = []
    for gorelka in hub.gorelka:
        new_devices.append(TempMainSensor(gorelka))
        new_devices.append(TempExtSensor(gorelka))
        new_devices.append(TempDiselSensor(gorelka))
        new_devices.append(TempOilSensor(gorelka))
        new_devices.append(FireSensor(gorelka))
        new_devices.append(StateSensor(gorelka))
    if new_devices:
        async_add_entities(new_devices)


# This base class shows the common properties and methods for a sensor as used in this
# example. See each sensor for further details about properties and methods that
# have been overridden.
class SensorBase(Entity):
    """Base representation of a Hello World Sensor."""

    should_poll = False

    def __init__(self, gorelka):
        """Initialize the sensor."""
        self._gorelka = gorelka

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

    async def async_added_to_hass(self):
        """Run when this Entity has been added to HA."""
        # Sensors should also register callbacks to HA when their state changes
        self._gorelka.register_callback(self.async_write_ha_state)

    async def async_will_remove_from_hass(self):
        """Entity being removed from hass."""
        # The opposite of async_added_to_hass. Remove any registered call backs here.
        self._gorelka.remove_callback(self.async_write_ha_state)


class TempMainSensor(SensorBase):
    """Representation of a Sensor."""

    # The class of this device. Note the value should come from the homeassistant.const
    # module. More information on the available devices classes can be seen here:
    # https://developers.home-assistant.io/docs/core/entity/sensor
    device_class = SensorDeviceClass.TEMPERATURE

    # The unit of measurement for this entity. As it's a DEVICE_CLASS_BATTERY, this
    # should be PERCENTAGE. A number of units are supported by HA, for some
    # examples, see:
    # https://developers.home-assistant.io/docs/core/entity/sensor#available-device-classes
    _attr_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, gorelka):
        """Initialize the sensor."""
        super().__init__(gorelka)

        # As per the sensor, this must be a unique value within this domain. This is done
        # by using the device ID, and appending "_battery"
        self._attr_unique_id = f"{self._gorelka.gorelka_id}_main"

        # The name of the entity
        self._attr_name = f"{self._gorelka.name} Main"

        self._state = self._gorelka.temp_main

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._gorelka.temp_main


class TempExtSensor(SensorBase):
    """Representation of a Sensor."""

    # The class of this device. Note the value should come from the homeassistant.const
    # module. More information on the available devices classes can be seen here:
    # https://developers.home-assistant.io/docs/core/entity/sensor
    device_class = SensorDeviceClass.TEMPERATURE

    # The unit of measurement for this entity. As it's a DEVICE_CLASS_BATTERY, this
    # should be PERCENTAGE. A number of units are supported by HA, for some
    # examples, see:
    # https://developers.home-assistant.io/docs/core/entity/sensor#available-device-classes
    _attr_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, gorelka):
        """Initialize the sensor."""
        super().__init__(gorelka)

        # As per the sensor, this must be a unique value within this domain. This is done
        # by using the device ID, and appending "_battery"
        self._attr_unique_id = f"{self._gorelka.gorelka_id}_ext"

        # The name of the entity
        self._attr_name = f"{self._gorelka.name} Ext"

        self._state = self._gorelka.temp_ext

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._gorelka.temp_ext


class TempDiselSensor(SensorBase):
    """Representation of a Sensor."""

    # The class of this device. Note the value should come from the homeassistant.const
    # module. More information on the available devices classes can be seen here:
    # https://developers.home-assistant.io/docs/core/entity/sensor
    device_class = SensorDeviceClass.TEMPERATURE

    # The unit of measurement for this entity. As it's a DEVICE_CLASS_BATTERY, this
    # should be PERCENTAGE. A number of units are supported by HA, for some
    # examples, see:
    # https://developers.home-assistant.io/docs/core/entity/sensor#available-device-classes
    _attr_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, gorelka):
        """Initialize the sensor."""
        super().__init__(gorelka)

        # As per the sensor, this must be a unique value within this domain. This is done
        # by using the device ID, and appending "_battery"
        self._attr_unique_id = f"{self._gorelka.gorelka_id}_disel"

        # The name of the entity
        self._attr_name = f"{self._gorelka.name} Disel"

        self._state = self._gorelka.temp_disel

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._gorelka.temp_disel


class TempOilSensor(SensorBase):
    """Representation of a Sensor."""

    # The class of this device. Note the value should come from the homeassistant.const
    # module. More information on the available devices classes can be seen here:
    # https://developers.home-assistant.io/docs/core/entity/sensor
    device_class = SensorDeviceClass.TEMPERATURE

    # The unit of measurement for this entity. As it's a DEVICE_CLASS_BATTERY, this
    # should be PERCENTAGE. A number of units are supported by HA, for some
    # examples, see:
    # https://developers.home-assistant.io/docs/core/entity/sensor#available-device-classes
    _attr_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, gorelka):
        """Initialize the sensor."""
        super().__init__(gorelka)

        # As per the sensor, this must be a unique value within this domain. This is done
        # by using the device ID, and appending "_battery"
        self._attr_unique_id = f"{self._gorelka.gorelka_id}_oil"

        # The name of the entity
        self._attr_name = f"{self._gorelka.name} Oil"

        self._state = self._gorelka.temp_oil

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._gorelka.temp_oil


class FireSensor(SensorBase):
    """Representation of a Sensor."""

    # The class of this device. Note the value should come from the homeassistant.const
    # module. More information on the available devices classes can be seen here:
    # https://developers.home-assistant.io/docs/core/entity/sensor
    device_class = SensorDeviceClass.ILLUMINANCE

    def __init__(self, gorelka):
        """Initialize the sensor."""
        super().__init__(gorelka)
        self._attr_icon = FIREICON

        # As per the sensor, this must be a unique value within this domain. This is done
        # by using the device ID, and appending "_battery"
        self._attr_unique_id = f"{self._gorelka.gorelka_id}_fire"

        # The name of the entity
        self._attr_name = f"{self._gorelka.name} Fire"

        self._state = self._gorelka.fire

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._gorelka.fire


class StateSensor(SensorBase):
    """Representation of a Sensor."""

    # The class of this device. Note the value should come from the homeassistant.const
    # module. More information on the available devices classes can be seen here:
    # https://developers.home-assistant.io/docs/core/entity/sensor
    device_class = SensorDeviceClass.ENUM

    def __init__(self, gorelka):
        """Initialize the sensor."""
        super().__init__(gorelka)

        self._attr_unique_id = f"{self._gorelka.gorelka_id}_state"

        # The name of the entity
        self._attr_name = f"{self._gorelka.name} State"
        self._attr_translation_key = "main_state"

        self._attr_options = ["work", "sleep", "heat_od"]
        self._attr_native_value = self._gorelka.main_status

    async def async_update(self) -> None:
        """Get the time and updates the states."""
        self._attr_native_value = self._gorelka.main_status
