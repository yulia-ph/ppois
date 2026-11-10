from datetime import datetime

from exceptions.InvalidCargoStateException import InvalidCargoStateException


class Waypoint:
    """A stop on a route."""

    STOP_PICKUP = "pickup"
    STOP_DELIVERY = "delivery"
    STOP_REST = "rest"

    VALID_STOPS = (STOP_PICKUP, STOP_DELIVERY, STOP_REST)

    def __init__(self, address, sequence: int, window_start: datetime, window_end: datetime, stop_type: str):
        if address is None:
            raise ValueError("Address must not be None")
        if sequence < 1:
            raise ValueError(f"Sequence must be at least 1, got {sequence}")
        if window_end <= window_start:
            raise ValueError("Window end must be after start")
        if stop_type not in Waypoint.VALID_STOPS:
            raise ValueError(f"Invalid stop type '{stop_type}'")
        self._address = address
        self._sequence = sequence
        self._window_start = window_start
        self._window_end = window_end
        self._stop_type = stop_type
        self._is_visited = False
        self._arrived_at = None

    @property
    def address(self):
        return self._address

    @property
    def sequence(self):
        return self._sequence

    @property
    def window_start(self):
        return self._window_start

    @property
    def window_end(self):
        return self._window_end

    @property
    def stop_type(self):
        return self._stop_type

    @property
    def is_visited(self):
        return self._is_visited

    def arrive(self, at: datetime = None):
        """Mark arrival."""
        if self._is_visited:
            raise InvalidCargoStateException(
                title=str(self._sequence),
                state="visited",
                reason="Waypoint already visited",
            )
        self._arrived_at = at or datetime.now()
        self._is_visited = True
        return True

    def depart(self):
        """Leave the waypoint. It must already have been arrived at."""
        if not self._is_visited:
            raise InvalidCargoStateException(
                title=str(self._sequence),
                state="pending",
                reason="Cannot depart before arrival",
            )
        return True

    def is_missed(self, now: datetime = None) -> bool:
        """Return True if the window has passed without a visit."""
        moment = now or datetime.now()
        return (not self._is_visited) and moment > self._window_end

    def reschedule(self, window_start: datetime, window_end: datetime):
        """Move the time window."""
        if self._is_visited:
            raise InvalidCargoStateException(
                title=str(self._sequence),
                state="visited",
                reason="Cannot reschedule a visited waypoint",
            )
        if window_end <= window_start:
            raise ValueError("Window end must be after start")
        self._window_start = window_start
        self._window_end = window_end
        return True
