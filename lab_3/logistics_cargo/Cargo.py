from exceptions.CargoOverweightException import CargoOverweightException
from exceptions.InvalidCargoStateException import InvalidCargoStateException


class Cargo:
    """Base class for freight."""

    STATUS_CREATED = "created"
    STATUS_PACKED = "packed"
    STATUS_IN_TRANSIT = "in_transit"
    STATUS_DELIVERED = "delivered"
    STATUS_DAMAGED = "damaged"

    VALID_STATUSES = (
        STATUS_CREATED,
        STATUS_PACKED,
        STATUS_IN_TRANSIT,
        STATUS_DELIVERED,
        STATUS_DAMAGED,
    )

    _counter = 0

    def __init__(self, weight: float, volume: float, origin, destination, declared_value: float = 0.0):
        if weight <= 0:
            raise ValueError(f"Weight must be positive, got {weight}")
        if volume <= 0:
            raise ValueError(f"Volume must be positive, got {volume}")
        if origin is None or destination is None:
            raise ValueError("Origin and destination must not be None")
        if declared_value < 0:
            raise ValueError(f"Declared value must be non-negative, got {declared_value}")
        Cargo._counter += 1
        self._tracking_id = f"CG-{Cargo._counter:06d}"
        self._weight = weight
        self._volume = volume
        self._status = Cargo.STATUS_CREATED
        self._declared_value = declared_value
        self._origin = origin
        self._destination = destination

    @property
    def tracking_id(self):
        return self._tracking_id

    @property
    def weight(self):
        return self._weight

    @property
    def volume(self):
        return self._volume

    @property
    def status(self):
        return self._status

    @property
    def declared_value(self):
        return self._declared_value

    @property
    def origin(self):
        return self._origin

    @property
    def destination(self):
        return self._destination

    def can_fit(self, limit_kg: float) -> bool:
        """Return True if this cargo is within `limit_kg`.

        Raises:
            CargoOverweightException: If the cargo is heavier than the limit.
        """
        if limit_kg <= 0:
            raise ValueError(f"Limit must be positive, got {limit_kg}")
        if self._weight > limit_kg:
            raise CargoOverweightException(weight=self._weight, limit=limit_kg)
        return True

    def pack(self):
        """Mark cargo as packed."""
        if self._status != Cargo.STATUS_CREATED:
            raise InvalidCargoStateException(
                title=self._tracking_id,
                state=self._status,
                reason="Only newly created cargo can be packed",
            )
        self._status = Cargo.STATUS_PACKED
        return True

    def unpack(self):
        """Unpack delivered or packed cargo."""
        if self._status not in (Cargo.STATUS_PACKED, Cargo.STATUS_DELIVERED):
            raise InvalidCargoStateException(
                title=self._tracking_id,
                state=self._status,
                reason="Cargo cannot be unpacked in this state",
            )
        self._status = Cargo.STATUS_CREATED
        return True

    def mark_damaged(self):
        """Mark cargo as damaged."""
        if self._status == Cargo.STATUS_DAMAGED:
            raise InvalidCargoStateException(
                title=self._tracking_id,
                state=self._status,
                reason="Cargo is already damaged",
            )
        self._status = Cargo.STATUS_DAMAGED
        return True

    def update_status(self, new_status: str):
        """Move cargo to a valid status."""
        if new_status not in Cargo.VALID_STATUSES:
            raise ValueError(f"Invalid status '{new_status}'")
        if self._status == Cargo.STATUS_DAMAGED and new_status != Cargo.STATUS_DAMAGED:
            raise InvalidCargoStateException(
                title=self._tracking_id,
                state=self._status,
                reason="Damaged cargo cannot change status",
            )
        self._status = new_status
        return True
