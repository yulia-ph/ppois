from exceptions.InvalidCargoStateException import InvalidCargoStateException


class Trailer:
    """A trailer that can be hitched to a truck."""

    TYPE_FLATBED = "flatbed"
    TYPE_REEFER = "reefer"
    TYPE_CURTAIN = "curtain"

    VALID_TYPES = (TYPE_FLATBED, TYPE_REEFER, TYPE_CURTAIN)

    def __init__(self, plate: str, capacity_kg: float, trailer_type: str):
        if not plate:
            raise ValueError("Plate must not be empty")
        if capacity_kg <= 0:
            raise ValueError(f"Capacity must be positive, got {capacity_kg}")
        if trailer_type not in Trailer.VALID_TYPES:
            raise ValueError(
                f"Invalid trailer type '{trailer_type}'. "
                f"Must be one of {Trailer.VALID_TYPES}"
            )
        self._plate = plate
        self._capacity_kg = capacity_kg
        self._trailer_type = trailer_type
        self._attached_to = None
        self._loaded_kg = 0.0

    @property
    def plate(self):
        return self._plate

    @property
    def capacity_kg(self):
        return self._capacity_kg

    @property
    def trailer_type(self):
        return self._trailer_type

    @property
    def attached_to(self):
        return self._attached_to

    @property
    def is_attached(self):
        return self._attached_to is not None

    def remaining_capacity(self) -> float:
        """Kilograms still available."""
        return self._capacity_kg - self._loaded_kg

    def attach(self, vehicle):
        """Record the vehicle this trailer is hitched to."""
        if vehicle is None:
            raise ValueError("Vehicle must not be None")
        if self._attached_to is not None:
            raise InvalidCargoStateException(
                title=self._plate,
                state="attached",
                reason="Trailer is already attached",
            )
        self._attached_to = vehicle
        return True

    def detach(self):
        """Clear the hitch."""
        if self._attached_to is None:
            raise InvalidCargoStateException(
                title=self._plate,
                state="free",
                reason="Trailer is not attached",
            )
        self._attached_to = None
        return True
