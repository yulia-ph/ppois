from exceptions.StorageCapacityExceededException import StorageCapacityExceededException
from museum_core.ClimateZone import ClimateZone
from museum_exhibits.Exhibit import Exhibit


class Storage:
    """A storage facility for exhibits not currently on display.

    Each storage has a fixed capacity (maximum number of exhibits) and
    can optionally have its own climate zone. Storage provides
    methods for placing, removing, and finding exhibits, as well as
    running an inventory reconciliation against a reference catalog.
    """

    def __init__(self, name: str, capacity: int):
        """Initialize a storage facility.

        Args:
            name: The storage name.
            capacity: Maximum number of exhibits. Must be positive.

        Raises:
            ValueError: If name is empty or capacity is not positive.
        """
        if not name:
            raise ValueError("Storage name must not be empty")
        if capacity <= 0:
            raise ValueError(f"Capacity must be positive, got {capacity}")
        self._name = name
        self._capacity = capacity
        self._exhibits = []
        self._climate_zone = None


    @property
    def name(self):
        return self._name

    @property
    def capacity(self):
        return self._capacity

    @property
    def exhibits(self):
        return list(self._exhibits)

    @property
    def climate_zone(self):
        return self._climate_zone

    @property
    def is_full(self):
        return len(self._exhibits) >= self._capacity

    @property
    def free_space(self):
        return self._capacity - len(self._exhibits)


    def place_exhibit(self, exhibit: Exhibit):
        """Place an exhibit into this storage.

        Args:
            exhibit: The exhibit to store. Must not be None.

        Raises:
            ValueError: If exhibit is None or already in this storage.
            StorageCapacityExceededException: If the storage is full.
        """
        if exhibit is None:
            raise ValueError("Exhibit must not be None")
        if self.is_full:
            raise StorageCapacityExceededException(
                storage_name=self._name,
                capacity=self._capacity,
            )
        if exhibit in self._exhibits:
            raise ValueError(
                f"Exhibit '{exhibit.inventory_number}' is already in storage '{self._name}'"
            )
        self._exhibits.append(exhibit)
        return True

    def remove_exhibit(self, exhibit: Exhibit):
        """Remove an exhibit from this storage.

        Args:
            exhibit: The exhibit to remove.

        Raises:
            ValueError: If the exhibit is not in this storage.
        """
        if exhibit not in self._exhibits:
            raise ValueError(
                f"Exhibit '{exhibit.inventory_number}' is not in storage '{self._name}'"
            )
        self._exhibits.remove(exhibit)
        return True

    def has_exhibit(self, exhibit: Exhibit) -> bool:
        """Return True if the exhibit is stored here."""
        return exhibit in self._exhibits

    def find_exhibit(self, inventory_number: str) -> Exhibit:
        """Find an exhibit by its inventory number.

        Args:
            inventory_number: The exhibit inventory number.

        Returns:
            The matching Exhibit.

        Raises:
            ValueError: If no exhibit with the given number is found.
        """
        for exhibit in self._exhibits:
            if exhibit.inventory_number == inventory_number:
                return exhibit
        raise ValueError(
            f"Exhibit '{inventory_number}' not found in storage '{self._name}'"
        )

    def set_climate_zone(self, zone: ClimateZone):
        """Attach a climate zone to this storage.

        Args:
            zone: The climate zone to attach. Must not be None.

        Raises:
            ValueError: If zone is None.
        """
        if zone is None:
            raise ValueError("Climate zone must not be None")
        self._climate_zone = zone
        return True

    def check_climate(self) -> bool:
        """Return True if the storage's climate is within norm.

        If no climate zone is attached, returns True (nothing to check).
        """
        if self._climate_zone is None:
            return True
        return self._climate_zone.is_within_norm()


    def run_inventory(self, catalog_exhibits: list) -> dict:
        """Reconcile storage contents against a reference catalog.

        Args:
            catalog_exhibits: The list of exhibits that should be
                present according to the catalog.

        Returns:
            A dict with keys:
                'missing': exhibits in the catalog but not in storage.
                'extra': exhibits in storage but not in the catalog.
                'is_clean': True if both lists are empty.
        """
        missing = [ex for ex in catalog_exhibits if ex not in self._exhibits]
        extra = [ex for ex in self._exhibits if ex not in catalog_exhibits]
        return {
            "missing": missing,
            "extra": extra,
            "is_clean": not missing and not extra,
        }