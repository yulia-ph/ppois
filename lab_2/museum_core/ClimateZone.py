from museum_core.Sensor import Sensor


class ClimateZone:
    """A climate zone inside a museum space.

    Represents the temperature and humidity conditions of a room,
    storage, or showcase. Each zone has target (norm) values and
    tolerances; deviations beyond tolerances mean the zone is out of
    norm and may trigger a climate-control alert.

    The zone is observed by one or more sensors, which read its values.
    """

    TEMP_MIN = -50.0
    TEMP_MAX = 50.0
    HUMIDITY_MIN = 0.0
    HUMIDITY_MAX = 100.0

    DEFAULT_TEMP_TOLERANCE = 2.0
    DEFAULT_HUMID_TOLERANCE = 5.0

    def __init__(self, norm_temperature: float, norm_humidity: float):
        """Initialize a climate zone with target values.

        Args:
            norm_temperature: Target temperature in degrees Celsius.
                Must be within [TEMP_MIN, TEMP_MAX].
            norm_humidity: Target humidity as a percentage.
                Must be within [HUMIDITY_MIN, HUMIDITY_MAX].

        Raises:
            ValueError: If norm values are outside physical bounds.
        """
        if not (ClimateZone.TEMP_MIN <= norm_temperature <= ClimateZone.TEMP_MAX):
            raise ValueError(
                f"Temperature {norm_temperature} is out of range "
                f"[{ClimateZone.TEMP_MIN}, {ClimateZone.TEMP_MAX}]"
            )
        if not (ClimateZone.HUMIDITY_MIN <= norm_humidity <= ClimateZone.HUMIDITY_MAX):
            raise ValueError(
                f"Humidity {norm_humidity} is out of range "
                f"[{ClimateZone.HUMIDITY_MIN}, {ClimateZone.HUMIDITY_MAX}]"
            )

        self._temperature = norm_temperature
        self._humidity = norm_humidity
        self._norm_temperature = norm_temperature
        self._norm_humidity = norm_humidity
        self._temp_tolerance = ClimateZone.DEFAULT_TEMP_TOLERANCE
        self._humid_tolerance = ClimateZone.DEFAULT_HUMID_TOLERANCE
        self._sensors = []

    @property
    def temperature(self):
        return self._temperature

    @property
    def humidity(self):
        return self._humidity

    @property
    def norm_temperature(self):
        return self._norm_temperature

    @property
    def norm_humidity(self):
        return self._norm_humidity

    @property
    def temp_tolerance(self):
        return self._temp_tolerance

    @property
    def humid_tolerance(self):
        return self._humid_tolerance

    @property
    def sensors(self):
        return list(self._sensors)

    def add_sensor(self, sensor: Sensor):
        """Attach a sensor to this climate zone.

        Args:
            sensor: The sensor to attach.

        Raises:
            ValueError: If the sensor is already attached.
        """
        if sensor in self._sensors:
            raise ValueError(f"Sensor '{sensor.id}' is already attached to this zone")
        self._sensors.append(sensor)
        return True

    def remove_sensor(self, sensor: Sensor):
        """Detach a sensor from this climate zone.

        Args:
            sensor: The sensor to detach.

        Raises:
            ValueError: If the sensor is not attached to this zone.
        """
        if sensor not in self._sensors:
            raise ValueError(f"Sensor '{sensor.id}' is not attached to this zone")
        self._sensors.remove(sensor)
        return True

    def monitor(self) -> tuple:
        """Return the current (temperature, humidity) as a tuple."""
        return self._temperature, self._humidity

    def adjust(self, temperature: float, humidity: float):
        """Set new current values for temperature and humidity.

        Args:
            temperature: New temperature in degrees Celsius.
            humidity: New humidity percentage.

        Raises:
            ValueError: If either value is outside physical bounds.
        """
        if not (ClimateZone.TEMP_MIN <= temperature <= ClimateZone.TEMP_MAX):
            raise ValueError(
                f"Temperature {temperature} is out of range "
                f"[{ClimateZone.TEMP_MIN}, {ClimateZone.TEMP_MAX}]"
            )
        if not (ClimateZone.HUMIDITY_MIN <= humidity <= ClimateZone.HUMIDITY_MAX):
            raise ValueError(
                f"Humidity {humidity} is out of range "
                f"[{ClimateZone.HUMIDITY_MIN}, {ClimateZone.HUMIDITY_MAX}]"
            )
        self._temperature = temperature
        self._humidity = humidity
        return True

    def is_within_norm(self) -> bool:
        """Return True if current values are within tolerances of the norm."""
        dt = abs(self._temperature - self._norm_temperature)
        dh = abs(self._humidity - self._norm_humidity)
        return dt <= self._temp_tolerance and dh <= self._humid_tolerance


    def set_tolerances(self, temp_tol: float, humid_tol: float):
        """Set the allowed temperature and humidity tolerances.

        Args:
            temp_tol: Temperature tolerance in degrees Celsius.
            humid_tol: Humidity tolerance in percent.

        Raises:
            ValueError: If either tolerance is negative.
        """
        if temp_tol < 0:
            raise ValueError(f"Temperature tolerance must be non-negative, got {temp_tol}")
        if humid_tol < 0:
            raise ValueError(f"Humidity tolerance must be non-negative, got {humid_tol}")
        self._temp_tolerance = temp_tol
        self._humid_tolerance = humid_tol
        return True