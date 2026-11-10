from exceptions.InvalidCargoStateException import InvalidCargoStateException


class Rack:
    """A rack inside a storage zone."""

    def __init__(self, code: str, zone, slots: int, max_weight: float):
        if not code:
            raise ValueError("Code must not be empty")
        if zone is None:
            raise ValueError("Zone must not be None")
        if slots <= 0:
            raise ValueError(f"Slots must be positive, got {slots}")
        if max_weight <= 0:
            raise ValueError(f"Max weight must be positive, got {max_weight}")
        self._code = code
        self._zone = zone
        self._slots = slots
        self._max_weight = max_weight
        self._occupied = []

    @property
    def code(self):
        return self._code

    @property
    def zone(self):
        return self._zone

    @property
    def slots(self):
        return self._slots

    @property
    def max_weight(self):
        return self._max_weight

    @property
    def occupied(self):
        return list(self._occupied)

    def remaining_weight(self) -> float:
        """Kilograms still available."""
        used = sum(item.weight for item in self._occupied)
        return self._max_weight - used

    def is_full(self) -> bool:
        """True if no free slots or no remaining weight."""
        return len(self._occupied) >= self._slots or self.remaining_weight() <= 0

    def place(self, cargo):
        """Put cargo on the rack."""
        if cargo is None:
            raise ValueError("Cargo must not be None")
        if self.is_full():
            raise InvalidCargoStateException(
                title=self._code,
                state="full",
                reason="Rack is full",
            )
        if cargo.weight > self.remaining_weight():
            raise InvalidCargoStateException(
                title=self._code,
                state="overweight",
                reason="Not enough remaining weight",
            )
        self._occupied.append(cargo)
        return True

    def remove(self, cargo):
        """Take cargo off the rack."""
        if cargo not in self._occupied:
            raise ValueError("Cargo is not on this rack")
        self._occupied.remove(cargo)
        return True
