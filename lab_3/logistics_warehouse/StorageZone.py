from exceptions.InvalidCargoStateException import InvalidCargoStateException


class StorageZone:
    """A climate or purpose zone inside a warehouse."""

    TYPE_AMBIENT = "ambient"
    TYPE_COLD = "cold"
    TYPE_HAZMAT = "hazmat"

    VALID_TYPES = (TYPE_AMBIENT, TYPE_COLD, TYPE_HAZMAT)

    def __init__(self, name: str, warehouse, zone_type: str, temperature: float):
        if not name:
            raise ValueError("Zone name must not be empty")
        if warehouse is None:
            raise ValueError("Warehouse must not be None")
        if zone_type not in StorageZone.VALID_TYPES:
            raise ValueError(f"Invalid zone type '{zone_type}'")
        self._name = name
        self._warehouse = warehouse
        self._zone_type = zone_type
        self._temperature = temperature
        self._racks = []
        self._is_locked = False

    @property
    def name(self):
        return self._name

    @property
    def warehouse(self):
        return self._warehouse

    @property
    def zone_type(self):
        return self._zone_type

    @property
    def temperature(self):
        return self._temperature

    @property
    def racks(self):
        return list(self._racks)

    @property
    def is_locked(self):
        return self._is_locked

    def lock(self):
        """Lock the zone."""
        self._is_locked = True
        return True

    def unlock(self):
        """Unlock the zone."""
        self._is_locked = False
        return True

    def add_rack(self, rack):
        """Add a rack."""
        if rack is None:
            raise ValueError("Rack must not be None")
        if rack in self._racks:
            raise ValueError("Rack is already in this zone")
        self._racks.append(rack)
        return True

    def check_temperature(self, expected: float, tolerance: float = 2.0) -> bool:
        """Return True if current temperature is within tolerance."""
        if self._is_locked:
            raise InvalidCargoStateException(
                title=self._name,
                state="locked",
                reason="Cannot check a locked zone",
            )
        return abs(self._temperature - expected) <= tolerance
