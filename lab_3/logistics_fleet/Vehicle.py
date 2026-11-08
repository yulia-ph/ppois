from exceptions.VehicleNotAvailableException import VehicleNotAvailableException
from exceptions.VehicleOverloadException import VehicleOverloadException


class Vehicle:
    """Base class for fleet vehicles."""

    STATUS_IDLE = "idle"
    STATUS_ON_TRIP = "on_trip"
    STATUS_MAINTENANCE = "maintenance"

    VALID_STATUSES = (STATUS_IDLE, STATUS_ON_TRIP, STATUS_MAINTENANCE)

    LICENSE_CATEGORY = "B"

    def __init__(
        self,
        plate: str,
        vin: str,
        capacity_kg: float,
        volume_m3: float,
    ):
        """Initialize a vehicle.

        Raises:
            ValueError: If plate/vin is empty or capacity/volume is not positive.
        """
        if not plate:
            raise ValueError("Plate must not be empty")
        if not vin:
            raise ValueError("VIN must not be empty")
        if capacity_kg <= 0:
            raise ValueError(f"Capacity must be positive, got {capacity_kg}")
        if volume_m3 <= 0:
            raise ValueError(f"Volume must be positive, got {volume_m3}")
        self._plate = plate
        self._vin = vin
        self._capacity_kg = capacity_kg
        self._volume_m3 = volume_m3
        self._status = Vehicle.STATUS_IDLE
        self._driver = None
        self._gps = None
        self._fuel_level = 100.0
        self._odometer = 0.0

    @property
    def plate(self):
        return self._plate

    @property
    def vin(self):
        return self._vin

    @property
    def capacity_kg(self):
        return self._capacity_kg

    @property
    def volume_m3(self):
        return self._volume_m3

    @property
    def status(self):
        return self._status

    @property
    def driver(self):
        return self._driver

    @property
    def gps(self):
        return self._gps

    @property
    def fuel_level(self):
        return self._fuel_level

    @property
    def odometer(self):
        return self._odometer

    def assign_driver(self, driver):
        """Assign a driver. The driver object must expose assign_vehicle."""
        if driver is None:
            raise ValueError("Driver must not be None")
        driver.assign_vehicle(self)
        self._driver = driver
        return True

    def start_trip(self):
        """Mark the vehicle as on a trip.

        Raises:
            VehicleNotAvailableException: If the vehicle is not idle.
        """
        if self._status != Vehicle.STATUS_IDLE:
            raise VehicleNotAvailableException(plate=self._plate, status=self._status)
        if self._fuel_level <= 0:
            raise VehicleNotAvailableException(plate=self._plate, status="empty_tank")
        self._status = Vehicle.STATUS_ON_TRIP
        return True

    def finish_trip(self, distance_km: float = 0.0):
        """Return the vehicle to idle and add odometer kilometres."""
        if self._status != Vehicle.STATUS_ON_TRIP:
            raise VehicleNotAvailableException(plate=self._plate, status=self._status)
        if distance_km < 0:
            raise ValueError(f"Distance must be non-negative, got {distance_km}")
        self._odometer += distance_km
        self._status = Vehicle.STATUS_IDLE
        return True

    def refuel(self, liters: float):
        """Add fuel. Level is capped at 100."""
        if liters <= 0:
            raise ValueError(f"Liters must be positive, got {liters}")
        self._fuel_level = min(100.0, self._fuel_level + liters)
        return True

    def can_load(self, cargo) -> bool:
        """Return True if cargo fits by weight and volume.

        Raises:
            ValueError: If cargo is None.
            VehicleOverloadException: If cargo exceeds capacity.
        """
        if cargo is None:
            raise ValueError("Cargo must not be None")
        if cargo.weight > self._capacity_kg:
            raise VehicleOverloadException(
                plate=self._plate,
                weight=cargo.weight,
                capacity=self._capacity_kg,
            )
        if cargo.volume > self._volume_m3:
            raise VehicleOverloadException(
                plate=self._plate,
                weight=cargo.volume,
                capacity=self._volume_m3,
            )
        return True

    def locate(self, gps):
        """Set the current GPS position."""
        if gps is None:
            raise ValueError("GPS position must not be None")
        self._gps = gps
        return True
