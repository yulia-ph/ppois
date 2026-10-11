

class Schedule:
    """A schedule of museum events.

    A schedule is a collection of Event instances with search and
    conflict-detection helpers. Two active (non-canceled) events
    conflict if they share the same date and venue.
    """

    def __init__(self):
        """Initialize an empty schedule."""
        self._events = []


    @property
    def events(self):
        return list(self._events)

    @property
    def is_empty(self):
        return len(self._events) == 0


    def add_event(self, event):
        """Add an event to the schedule.

        Args:
            event: The event. Must not be None and must not already be
                in the schedule.

        Raises:
            ValueError: If event is None or already present.
        """
        if event is None:
            raise ValueError("Event must not be None")
        if event in self._events:
            raise ValueError(
                f"Event '{event.title}' is already in the schedule"
            )
        self._events.append(event)
        return True

    def remove_event(self, event):
        """Remove an event from the schedule.

        Args:
            event: The event. Must not be None and must be in the
                schedule.

        Raises:
            ValueError: If event is None or not present.
        """
        if event is None:
            raise ValueError("Event must not be None")
        if event not in self._events:
            raise ValueError(
                f"Event '{event.title}' is not in the schedule"
            )
        self._events.remove(event)
        return True

    def clear(self):
        """Remove all events from the schedule.

        Idempotent: clearing an already empty schedule is not an error.
        """
        self._events.clear()
        return True


    def get_events_for_day(self, date_):
        """Return all events on the given date."""
        return [e for e in self._events if e.date == date_]


    def find_conflicts(self):
        """Return pairs of active events that share a date and venue.

        Canceled events are ignored. Returns a list of (a, b) tuples
        where `a` is the earlier-added event.
        """
        conflicts = []
        seen = {}
        for event in self._events:
            if event.is_cancelled:
                continue
            key = (event.date, event.venue)
            if key in seen:
                conflicts.append((seen[key], event))
            else:
                seen[key] = event
        return conflicts