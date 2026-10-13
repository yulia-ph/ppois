from exceptions.BookingConflictException import BookingConflictException
from museum_core.Showcase import Showcase


class Hall:
    """An exhibition hall inside a museum building.

    A hall is a physical space that contains showcases and can host at
    most one exhibition at a time. The hall knows its current
    exhibition and can be queried for capacity, occupancy, and the
    number of exhibits on display.
    """

    SQUARE_METERS_PER_VISITOR = 2.0

    def __init__(self, number: int, area: float):
        """Initialize a hall.

        Args:
            number: The hall number, unique within a building.
            area: The floor area in square meters.

        Raises:
            ValueError: If area is not positive.
        """
        if area <= 0:
            raise ValueError(f"Hall area must be positive, got {area}")
        self._number = number
        self._area = area
        self._showcases = []
        self._current_exhibition = None

    @property
    def number(self):
        return self._number

    @property
    def area(self):
        return self._area

    @property
    def showcases(self):
        return list(self._showcases)

    @property
    def current_exhibition(self):
        return self._current_exhibition

    @property
    def is_busy(self):
        return self._current_exhibition is not None

    def add_showcase(self, showcase: Showcase):
        """Add a showcase to this hall.

        Args:
            showcase: The showcase to add.

        Raises:
            ValueError: If the showcase is already in this hall.
        """
        if showcase in self._showcases:
            raise ValueError(
                f"Showcase '{showcase.inventory_number}' is already in hall {self._number}"
            )
        self._showcases.append(showcase)
        return True

    def remove_showcase(self, showcase: Showcase):
        """Remove a showcase from this hall.

        Args:
            showcase: The showcase to remove.

        Raises:
            ValueError: If the showcase is not in this hall.
        """
        if showcase not in self._showcases:
            raise ValueError(
                f"Showcase '{showcase.inventory_number}' is not in hall {self._number}"
            )
        self._showcases.remove(showcase)
        return True


    def set_exhibition(self, exhibition):
        """Assign an exhibition to this hall.

        A hall can host only one exhibition at a time.

        Args:
            exhibition: The exhibition to host. Must not be None.

        Raises:
            ValueError: If the exhibition is None.
            BookingConflictException: If the hall already hosts an exhibition.
        """
        if exhibition is None:
            raise ValueError("Exhibition must not be None")
        if self._current_exhibition is not None:
            raise BookingConflictException(
                f"Hall {self._number} already hosts exhibition "
                f"'{self._current_exhibition.title}'"
            )
        self._current_exhibition = exhibition
        return True

    def clear_exhibition(self):
        """Remove the current exhibition from this hall.

        Idempotent: calling on an empty hall is not an error.
        """
        self._current_exhibition = None
        return True

    def calculate_capacity(self) -> int:
        """Return the maximum number of visitors this hall can hold.

        Computed from the area and SQUARE_METERS_PER_VISITOR.
        """
        return int(self._area / Hall.SQUARE_METERS_PER_VISITOR)

    def count_exhibits(self) -> int:
        """Return the number of exhibits currently on display."""
        count = 0
        for showcase in self._showcases:
            if showcase.exhibit is not None:
                count += 1
        return count

    def is_full(self, current_visitors: int) -> bool:
        """Return True if the given number of visitors exceeds capacity.

        Args:
            current_visitors: The number of visitors currently in the hall.
        """
        return current_visitors >= self.calculate_capacity()