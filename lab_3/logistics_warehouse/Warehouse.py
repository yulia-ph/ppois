from exceptions.WarehouseCapacityExceededException import WarehouseCapacityExceededException
from logistics_warehouse.InventoryCount import InventoryCount


class Warehouse:
    """A warehouse that holds cargo by volume."""

    def __init__(self, name: str, address, capacity_m3: float):
        if not name:
            raise ValueError("Warehouse name must not be empty")
        if address is None:
            raise ValueError("Address must not be None")
        if capacity_m3 <= 0:
            raise ValueError(f"Capacity must be positive, got {capacity_m3}")
        self._name = name
        self._address = address
        self._capacity_m3 = capacity_m3
        self._zones = []
        self._used_volume = 0.0
        self._cargo = []

    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self._address

    @property
    def capacity_m3(self):
        return self._capacity_m3

    @property
    def zones(self):
        return list(self._zones)

    @property
    def used_volume(self):
        return self._used_volume

    def remaining_capacity(self) -> float:
        """Cubic metres still free."""
        return self._capacity_m3 - self._used_volume

    def add_zone(self, zone):
        """Add a storage zone."""
        if zone is None:
            raise ValueError("Zone must not be None")
        if zone in self._zones:
            raise ValueError("Zone is already in this warehouse")
        self._zones.append(zone)
        return True

    def receive(self, cargo):
        """Accept cargo into the warehouse.

        Raises:
            WarehouseCapacityExceededException: If there is no room.
        """
        if cargo is None:
            raise ValueError("Cargo must not be None")
        if cargo in self._cargo:
            raise ValueError("Cargo is already in this warehouse")
        if cargo.volume > self.remaining_capacity():
            raise WarehouseCapacityExceededException(
                warehouse_name=self._name,
                capacity=self._capacity_m3,
            )
        self._cargo.append(cargo)
        self._used_volume += cargo.volume
        return True

    def ship(self, cargo):
        """Remove cargo from the warehouse."""
        if cargo not in self._cargo:
            raise ValueError("Cargo is not in this warehouse")
        self._cargo.remove(cargo)
        self._used_volume -= cargo.volume
        return True

    def find_cargo(self, tracking_id: str = None):
        """Return all cargo, or the item with `tracking_id`."""
        if tracking_id is None:
            return list(self._cargo)
        for item in self._cargo:
            if item.tracking_id == tracking_id:
                return item
        raise ValueError(f"Cargo '{tracking_id}' not found")

    def run_inventory(self, catalog):
        """Reconcile stored cargo against a catalog via InventoryCount.diff."""
        if catalog is None:
            raise ValueError("Catalog must not be None")
        missing, extra = InventoryCount.diff(self._cargo, catalog)
        return {
            "missing": missing,
            "extra": extra,
            "is_clean": not missing and not extra,
        }
