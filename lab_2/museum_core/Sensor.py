from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from museum_core.ClimateZone import ClimateZone


class SensorType(Enum):
    """The physical quantity a sensor measures."""

    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    MOTION = "motion"


class Sensor:
    """A sensor installed in a climate zone.

    A sensor reads a physical value (temperature or humidity) from its
    attached climate zone, or reports motion. It can be calibrated
    against a reference value and can signal an alert when the zone is
    out of norm.

    Motion sensors do not participate in climate monitoring.
    """

    MIN_REFERENCE = -100.0
    MAX_REFERENCE = 100.0
    INITIAL_VALUE = 0.0

    def __init__(self, sensor_id: str, type_: SensorType, zone: ClimateZone):
        """Initialize a sensor.

        Args:
            sensor_id: A unique sensor identifier.
            type_: The type of quantity the sensor measures.
            zone: The climate zone the sensor is attached to.

        Raises:
            ValueError: If sensor_id is empty or zone is None.
            TypeError: If type_ is not a SensorType instance.
        """
        if not sensor_id:
            raise ValueError("Sensor id must not be empty")
        if not isinstance(type_, SensorType):
            raise TypeError(
                f"type_ must be a SensorType, got {type(type_).__name__}"
            )
        if zone is None:
            raise ValueError("Climate zone must not be None")

        self._id = sensor_id
        self._type = type_
        self._zone = zone
        self._value = Sensor.INITIAL_VALUE
        self._is_calibrated = False

    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return self._type

    @property
    def zone(self):
        return self._zone

    @property
    def value(self):
        return self._value

    @property
    def is_calibrated(self):
        return self._is_calibrated

    def read_value(self) -> float:
        """Read the current value from the attached climate zone.

        Temperature sensors return the zone's temperature, humidity
        sensors return the zone's humidity. Motion sensors always
        return 0.0 (motion has no numeric reading in this model).

        Returns:
            The current sensor value.
        """
        temperature, humidity = self._zone.monitor()
        if self._type == SensorType.TEMPERATURE:
            self._value = temperature
        elif self._type == SensorType.HUMIDITY:
            self._value = humidity
        elif self._type == SensorType.MOTION:
            self._value = Sensor.INITIAL_VALUE
        return self._value

    def send_alert(self) -> bool:
        """Return True if this sensor should raise a climate alert.

        Motion sensors never raise climate alerts. Temperature and
        humidity sensors raise an alert when the attached zone is out
        of norm.
        """
        if self._type == SensorType.MOTION:
            return False
        return not self._zone.is_within_norm()

    def calibrate(self, reference: float):
        """Calibrate the sensor against a reference value.

        Args:
            reference: The reference value to write into the sensor.

        Raises:
            ValueError: If reference is outside [MIN_REFERENCE, MAX_REFERENCE].
        """
        if not (Sensor.MIN_REFERENCE <= reference <= Sensor.MAX_REFERENCE):
            raise ValueError(
                f"Reference {reference} is out of range "
                f"[{Sensor.MIN_REFERENCE}, {Sensor.MAX_REFERENCE}]"
            )
        self._value = reference
        self._is_calibrated = True
        return True

    def reset(self):
        """Reset the sensor value to zero and clear the calibration flag."""
        self._value = self._value = Sensor.INITIAL_VALUE
        self._is_calibrated = False
        return True