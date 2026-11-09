from datetime import date

from exceptions.InvalidCargoStateException import InvalidCargoStateException
from logistics_people.Employee import Employee


class WarehouseWorker(Employee):
    """A warehouse picker / forklift operator."""

    def __init__(self, name: str, salary: float, hire_date: date, warehouse, forklift_certified: bool = False):
        super().__init__(name, salary, hire_date)
        if warehouse is None:
            raise ValueError("Warehouse must not be None")
        self._warehouse = warehouse
        self._forklift_certified = forklift_certified
        self._current_zone = None

    @property
    def warehouse(self):
        return self._warehouse

    @property
    def forklift_certified(self):
        return self._forklift_certified

    @property
    def current_zone(self):
        return self._current_zone

    def pick_item(self, cargo):
        """Pick cargo from the warehouse."""
        if cargo is None:
            raise ValueError("Cargo must not be None")
        return self._warehouse.ship(cargo)

    def put_away(self, cargo):
        """Put cargo into the warehouse."""
        if cargo is None:
            raise ValueError("Cargo must not be None")
        return self._warehouse.receive(cargo)

    def operate_forklift(self, zone):
        """Move to a zone with a forklift."""
        if not self._forklift_certified:
            raise InvalidCargoStateException(
                title=self.name,
                state="no_certificate",
                reason="Worker is not forklift certified",
            )
        if zone is None:
            raise ValueError("Zone must not be None")
        self._current_zone = zone
        return True

    def count_items(self) -> int:
        """Count cargo currently in the warehouse."""
        return len(self._warehouse.find_cargo())
