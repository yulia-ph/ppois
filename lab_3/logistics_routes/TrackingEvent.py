from datetime import datetime


class TrackingEvent:
    """A GPS ping or delay event on a trip."""

    TYPE_POSITION = "position"
    TYPE_DELAY = "delay"
    TYPE_ARRIVAL = "arrival"

    VALID_TYPES = (TYPE_POSITION, TYPE_DELAY, TYPE_ARRIVAL)

    def __init__(self, trip, position, event_type: str):
        if trip is None:
            raise ValueError("Trip must not be None")
        if position is None:
            raise ValueError("Position must not be None")
        if event_type not in TrackingEvent.VALID_TYPES:
            raise ValueError(f"Invalid event type '{event_type}'")
        self._trip = trip
        self._position = position
        self._timestamp = datetime.now()
        self._event_type = event_type
        self._recorded = False

    @property
    def trip(self):
        return self._trip

    @property
    def position(self):
        return self._position

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def event_type(self):
        return self._event_type

    def record(self):
        """Mark the event as recorded and update the vehicle GPS."""
        self._recorded = True
        self._trip.vehicle.locate(self._position)
        return True

    def is_delay(self) -> bool:
        """Return True if this event is a delay."""
        return self._event_type == TrackingEvent.TYPE_DELAY

    def describe(self) -> str:
        """One-line description."""
        return (
            f"{self._event_type} at {self._position.latitude:.4f},"
            f"{self._position.longitude:.4f}"
        )
