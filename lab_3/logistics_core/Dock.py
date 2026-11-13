from exceptions.HazardousRestrictionException import HazardousRestrictionException


class Dock:
    """A loading dock at a terminal."""

    MIN_TANKER_LENGTH = 12.0

    def __init__(self, number: int, length_m: float, terminal=None):
        """Initialize a dock.

        Raises:
            ValueError: If number is not positive or length is not positive.
        """
        if number <= 0:
            raise ValueError(f"Dock number must be positive, got {number}")
        if length_m <= 0:
            raise ValueError(f"Dock length must be positive, got {length_m}")
        self._number = number
        self._length_m = length_m
        self._current_vehicle = None
        self._is_occupied = False
        self._terminal = terminal

    @property
    def number(self):
        return self._number

    @property
    def length_m(self):
        return self._length_m

    @property
    def current_vehicle(self):
        return self._current_vehicle

    @property
    def is_occupied(self):
        return self._is_occupied

    @property
    def terminal(self):
        return self._terminal

    def is_free(self) -> bool:
        """Return True if no vehicle is at the dock."""
        return not self._is_occupied

    def can_accept(self, vehicle) -> bool:
        """Return True if the dock can take this vehicle.

        Raises:
            ValueError: If vehicle is None.
            HazardousRestrictionException: If a dirty tanker does not fit.
        """
        if vehicle is None:
            raise ValueError("Vehicle must not be None")
        if self._is_occupied:
            return False
        chemical = getattr(vehicle, "chemical_class", None)
        cleaned = getattr(vehicle, "is_cleaned", True)
        if chemical and not cleaned:
            raise HazardousRestrictionException(
                reason="Uncleaned tanker cannot use a dock",
            )
        tank_volume = getattr(vehicle, "tank_volume", None)
        if tank_volume is not None and self._length_m < Dock.MIN_TANKER_LENGTH:
            raise HazardousRestrictionException(
                reason="Dock is too short for a tanker",
            )
        return True

    def occupy(self, vehicle):
        """Park a vehicle at this dock.

        Raises:
            ValueError: If vehicle is None.
            HazardousRestrictionException: Propagated from can_accept.
        """
        if not self.can_accept(vehicle):
            raise ValueError(f"Dock {self._number} cannot accept this vehicle")
        self._current_vehicle = vehicle
        self._is_occupied = True
        return True

    def release(self):
        """Free the dock.

        Idempotent if already free.
        """
        self._current_vehicle = None
        self._is_occupied = False
        return True
