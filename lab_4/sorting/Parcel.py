class Parcel:
    """A small user type for sort demos: destination and weight."""

    def __init__(self, destination: str, weight: int):
        if not destination:
            raise ValueError("Destination must not be empty")
        if weight <= 0:
            raise ValueError(f"Weight must be positive, got {weight}")
        self._destination = destination
        self._weight = weight

    @property
    def destination(self):
        return self._destination

    @property
    def weight(self):
        return self._weight

    def __eq__(self, other):
        if not isinstance(other, Parcel):
            return NotImplemented
        return self._weight == other._weight and self._destination == other._destination

    def __lt__(self, other):
        """Lighter first; same weight compares destination alphabetically."""
        if not isinstance(other, Parcel):
            return NotImplemented
        if self._weight != other._weight:
            return self._weight < other._weight
        return self._destination < other._destination

    def __repr__(self):
        return f"Parcel({self._destination!r}, {self._weight})"
