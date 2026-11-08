from datetime import date


class FuelLog:
    """A fuel fill-up recorded for a vehicle."""

    ANOMALY_LITERS_PER_100KM = 80.0

    def __init__(self, vehicle, liters: float, cost: float, station: str, odometer: float):
        if vehicle is None:
            raise ValueError("Vehicle must not be None")
        if liters <= 0:
            raise ValueError(f"Liters must be positive, got {liters}")
        if cost < 0:
            raise ValueError(f"Cost must be non-negative, got {cost}")
        if not station:
            raise ValueError("Station must not be empty")
        if odometer < 0:
            raise ValueError(f"Odometer must be non-negative, got {odometer}")
        self._vehicle = vehicle
        self._liters = liters
        self._cost = cost
        self._station = station
        self._date = date.today()
        self._odometer = odometer
        self._recorded = False

    @property
    def vehicle(self):
        return self._vehicle

    @property
    def liters(self):
        return self._liters

    @property
    def cost(self):
        return self._cost

    @property
    def station(self):
        return self._station

    @property
    def date(self):
        return self._date

    @property
    def odometer(self):
        return self._odometer

    def record(self):
        """Mark this fill-up as recorded on the vehicle."""
        self._recorded = True
        self._vehicle.refuel(self._liters)
        return True

    def consumption_per_100km(self, previous_odometer: float) -> float:
        """Litres per 100 km since the previous odometer reading."""
        distance = self._odometer - previous_odometer
        if distance <= 0:
            raise ValueError("Odometer must be greater than the previous reading")
        return self._liters / distance * 100.0

    def is_anomaly(self, previous_odometer: float) -> bool:
        """Return True if consumption looks unreasonably high."""
        return self.consumption_per_100km(previous_odometer) > FuelLog.ANOMALY_LITERS_PER_100KM
