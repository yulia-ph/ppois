from datetime import date

from exceptions.InvalidCargoStateException import InvalidCargoStateException


class MaintenanceRecord:
    """Work done on a vehicle by a mechanic."""

    STATUS_OPEN = "open"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_DONE = "done"

    def __init__(self, vehicle, mechanic, description: str, cost: float):
        if vehicle is None:
            raise ValueError("Vehicle must not be None")
        if mechanic is None:
            raise ValueError("Mechanic must not be None")
        if not description:
            raise ValueError("Description must not be empty")
        if cost < 0:
            raise ValueError(f"Cost must be non-negative, got {cost}")
        self._vehicle = vehicle
        self._mechanic = mechanic
        self._date = date.today()
        self._description = description
        self._cost = cost
        self._status = MaintenanceRecord.STATUS_OPEN
        self._parts = []

    @property
    def vehicle(self):
        return self._vehicle

    @property
    def mechanic(self):
        return self._mechanic

    @property
    def date(self):
        return self._date

    @property
    def description(self):
        return self._description

    @property
    def cost(self):
        return self._cost

    @property
    def status(self):
        return self._status

    def start_work(self):
        """Start the job."""
        if self._status != MaintenanceRecord.STATUS_OPEN:
            raise InvalidCargoStateException(
                title=self._vehicle.plate,
                state=self._status,
                reason="Maintenance is not open",
            )
        self._status = MaintenanceRecord.STATUS_IN_PROGRESS
        self._vehicle._status = "maintenance"
        return True

    def add_part(self, part: str, price: float):
        """Add a spare part to the bill."""
        if not part:
            raise ValueError("Part name must not be empty")
        if price < 0:
            raise ValueError(f"Price must be non-negative, got {price}")
        if self._status == MaintenanceRecord.STATUS_DONE:
            raise InvalidCargoStateException(
                title=self._vehicle.plate,
                state=self._status,
                reason="Cannot add parts to a completed job",
            )
        self._parts.append((part, price))
        self._cost += price
        return True

    def complete(self):
        """Finish the job and return the vehicle to idle."""
        if self._status != MaintenanceRecord.STATUS_IN_PROGRESS:
            raise InvalidCargoStateException(
                title=self._vehicle.plate,
                state=self._status,
                reason="Maintenance is not in progress",
            )
        self._status = MaintenanceRecord.STATUS_DONE
        self._vehicle._status = "idle"
        return True

    def estimate_downtime(self) -> int:
        """Rough downtime in hours: one hour per part, minimum two."""
        return max(2, len(self._parts) + 1)
