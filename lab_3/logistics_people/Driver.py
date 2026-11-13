from datetime import date, timedelta

from exceptions.DriverNotAvailableException import DriverNotAvailableException
from logistics_people.Employee import Employee


class Driver(Employee):
    """A driver with a license and hour log."""

    MAX_HOURS = 9.0

    def __init__(self, name: str, salary: float, hire_date: date, license):
        super().__init__(name, salary, hire_date)
        if license is None:
            raise ValueError("License must not be None")
        self._license = license
        self._assigned_vehicle = None
        self._hours_driven = 0.0
        self._is_available = True
        self._rest_until = None

    @property
    def license(self):
        return self._license

    @property
    def assigned_vehicle(self):
        return self._assigned_vehicle

    @property
    def hours_driven(self):
        return self._hours_driven

    @property
    def is_available(self):
        return self._is_available

    @property
    def rest_until(self):
        return self._rest_until

    def start_shift(self):
        """Start a driving shift."""
        if not self._is_available:
            raise DriverNotAvailableException(name=self.name, reason="not available")
        if self.on_leave:
            raise DriverNotAvailableException(name=self.name, reason="on leave")
        self._hours_driven = 0.0
        return True

    def end_shift(self):
        """End the shift and put the driver on rest until tomorrow."""
        self._is_available = False
        self._rest_until = date.today() + timedelta(days=1)
        return True

    def assign_vehicle(self, vehicle):
        """Assign a vehicle if the license covers its category."""
        if vehicle is None:
            raise ValueError("Vehicle must not be None")
        category = getattr(vehicle, "LICENSE_CATEGORY", "B")
        self._license.covers_category(category)
        self._assigned_vehicle = vehicle
        return True

    def log_hours(self, hours: float):
        """Add driving hours. Over the limit the driver becomes unavailable."""
        if hours <= 0:
            raise ValueError(f"Hours must be positive, got {hours}")
        self._hours_driven += hours
        if self._hours_driven > Driver.MAX_HOURS:
            self._is_available = False
        return True

    def can_take_order(self) -> bool:
        """Return True if the driver can take a new order.

        Raises:
            DriverNotAvailableException: If the driver cannot take work.
        """
        if self.on_leave or not self._is_available:
            raise DriverNotAvailableException(name=self.name, reason="not available")
        if self._hours_driven >= Driver.MAX_HOURS:
            raise DriverNotAvailableException(name=self.name, reason="hours limit")
        return True
