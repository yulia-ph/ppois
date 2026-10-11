from exceptions.InvalidExhibitStateException import InvalidExhibitStateException


class Event:
    """A museum event: lecture, workshop, concert, or other.

    An event has a fixed date, venue, and capacity. Visitors can
    register and unregister while the event is not cancelled and not
    full. Cancelling an event clears all registrations.

    Two active events conflict if they share the same date and venue;
    this is checked by Schedule.find_conflicts().
    """

    TYPE_LECTURE = "lecture"
    TYPE_WORKSHOP = "workshop"
    TYPE_CONCERT = "concert"
    TYPE_OTHER = "other"

    VALID_TYPES = (TYPE_LECTURE, TYPE_WORKSHOP, TYPE_CONCERT, TYPE_OTHER)

    def __init__(self, title: str, type_: str, date_, venue: str, capacity: int):
        """Initialize an event.

        Args:
            title: The event title. Must not be empty.
            type_: One of VALID_TYPES.
            date_: The event date. Must not be None.
            venue: The venue name. Must not be empty.
            capacity: Maximum number of visitors. Must be positive.

        Raises:
            ValueError: If any argument is invalid.
        """
        if not title:
            raise ValueError("Event title must not be empty")
        if type_ not in Event.VALID_TYPES:
            raise ValueError(
                f"Invalid event type '{type_}'. Must be one of {Event.VALID_TYPES}"
            )
        if date_ is None:
            raise ValueError("Event date must not be None")
        if not venue:
            raise ValueError("Event venue must not be empty")
        if capacity <= 0:
            raise ValueError(f"Capacity must be positive, got {capacity}")

        self._title = title
        self._type = type_
        self._date = date_
        self._venue = venue
        self._capacity = capacity
        self._registered = []
        self._is_cancelled = False

    @property
    def title(self):
        return self._title

    @property
    def type(self):
        return self._type

    @property
    def date(self):
        return self._date

    @property
    def venue(self):
        return self._venue

    @property
    def capacity(self):
        return self._capacity

    @property
    def registered(self):
        return list(self._registered)

    @property
    def is_cancelled(self):
        return self._is_cancelled

    @property
    def is_full(self):
        return len(self._registered) >= self._capacity

    @property
    def is_active(self):
        return not self._is_cancelled


    def register(self, visitor):
        """Register a visitor for this event.

        Args:
            visitor: The visitor. Must not be None.

        Raises:
            ValueError: If visitor is None or already registered.
            InvalidExhibitStateException: If the event is cancelled or full.
        """
        if visitor is None:
            raise ValueError("Visitor must not be None")
        if self._is_cancelled:
            raise InvalidExhibitStateException(
                exhibit_title=self._title,
                state="cancelled",
                reason="Cannot register for a cancelled event",
            )
        if self.is_full:
            raise InvalidExhibitStateException(
                exhibit_title=self._title,
                state="full",
                reason="Event has no free seats",
            )
        if visitor in self._registered:
            raise ValueError(
                f"Visitor '{visitor.name}' is already registered for '{self._title}'"
            )
        self._registered.append(visitor)
        return True

    def unregister(self, visitor):
        """Remove a visitor from the event.

        Args:
            visitor: The visitor. Must not be None.

        Raises:
            ValueError: If visitor is None or not registered.
        """
        if visitor is None:
            raise ValueError("Visitor must not be None")
        if visitor not in self._registered:
            raise ValueError(
                f"Visitor '{visitor.name}' is not registered for '{self._title}'"
            )
        self._registered.remove(visitor)
        return True


    def cancel(self):
        """Cancel the event and clear all registrations.

        Idempotent: cancelling an already cancelled event is not an error.
        """
        self._is_cancelled = True
        self._registered.clear()
        return True


    def count_registered(self) -> int:
        """Return the number of registered visitors."""
        return len(self._registered)

    def free_seats(self) -> int:
        """Return the number of free seats."""
        return self._capacity - len(self._registered)