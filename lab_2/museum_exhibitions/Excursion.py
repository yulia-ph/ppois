from exceptions.InvalidExhibitStateException import InvalidExhibitStateException


class Excursion:
    """A guided tour through a sequence of halls.

    An excursion has a route (list of halls), a guide, a start time,
    and a duration. Visitors can join before the tour finishes. The
    route and guide cannot be changed once the tour has started.

    The tour moves through two states: started (after start()), and
    finished (after finish()). Use is_active() to check "started and
    not yet finished".
    """

    _counter = 0

    def __init__(self, route_points, guide, start_time, duration_minutes: int):
        """Initialize an excursion.

        Args:
            route_points: Initial route as an iterable of halls
                (they may be empty).
            guide: The tour guide. Must not be None.
            start_time: The planned start time. Must not be None.
            duration_minutes: Duration in minutes. Must be positive.

        Raises:
            ValueError: If guide or start_time is None, or duration is
                not positive.
        """
        if guide is None:
            raise ValueError("Guide must not be None")
        if start_time is None:
            raise ValueError("Start time must not be None")
        if duration_minutes <= 0:
            raise ValueError(
                f"Duration must be positive, got {duration_minutes}"
            )

        Excursion._counter += 1
        self._id = f"EXC-{Excursion._counter:04d}"
        self._route_points = list(route_points) if route_points else []
        self._guide = guide
        self._start_time = start_time
        self._duration_minutes = duration_minutes
        self._visitors = []
        self._is_started = False
        self._is_finished = False


    @property
    def id(self):
        return self._id

    @property
    def route_points(self):
        return list(self._route_points)

    @property
    def guide(self):
        return self._guide

    @property
    def start_time(self):
        return self._start_time

    @property
    def duration_minutes(self):
        return self._duration_minutes

    @property
    def visitors(self):
        return list(self._visitors)

    @property
    def is_started(self):
        return self._is_started

    @property
    def is_finished(self):
        return self._is_finished

    @property
    def is_active(self):
        return self._is_started and not self._is_finished


    def add_route_point(self, hall):
        """Add a hall to the route.

        Args:
            hall: The hall. Must not be None and must not already be
                in the route.

        Raises:
            ValueError: If hall is None or already in the route.
            InvalidExhibitStateException: If the tour has already started.
        """
        if hall is None:
            raise ValueError("Hall must not be None")
        if self._is_started:
            raise InvalidExhibitStateException(
                exhibit_title=self._id,
                state="started",
                reason="Cannot modify route after the tour has started",
            )
        if hall in self._route_points:
            raise ValueError(f"Hall '{hall.number}' is already in the route")
        self._route_points.append(hall)
        return True

    def remove_route_point(self, hall):
        """Remove a hall from the route.

        Args:
            hall: The hall. Must be in the route.

        Raises:
            ValueError: If hall is None or not in the route.
            InvalidExhibitStateException: If the tour has already started.
        """
        if hall is None:
            raise ValueError("Hall must not be None")
        if self._is_started:
            raise InvalidExhibitStateException(
                exhibit_title=self._id,
                state="started",
                reason="Cannot modify route after the tour has started",
            )
        if hall not in self._route_points:
            raise ValueError(f"Hall '{hall.number}' is not in the route")
        self._route_points.remove(hall)
        return True

    def optimize_route(self):
        """Sort route points by hall number.

        Raises:
            InvalidExhibitStateException: If the tour has already started.
        """
        if self._is_started:
            raise InvalidExhibitStateException(
                exhibit_title=self._id,
                state="started",
                reason="Cannot optimize route after the tour has started",
            )
        self._route_points.sort(key=lambda h: h.number)
        return True

    def count_points(self) -> int:
        """Return the number of route points."""
        return len(self._route_points)


    def add_visitor(self, visitor):
        """Add a visitor to the excursion.

        Args:
            visitor: The visitor. Must not be None and must not already
                be in the excursion.

        Raises:
            ValueError: If visitor is None or already added.
            InvalidExhibitStateException: If the tour has already finished.
        """
        if visitor is None:
            raise ValueError("Visitor must not be None")
        if self._is_finished:
            raise InvalidExhibitStateException(
                exhibit_title=self._id,
                state="finished",
                reason="Cannot add visitors to a finished tour",
            )
        if visitor in self._visitors:
            raise ValueError(
                f"Visitor '{visitor.name}' is already in this excursion"
            )
        self._visitors.append(visitor)
        return True


    def count_visitors(self) -> int:
        """Return the number of visitors on the excursion."""
        return len(self._visitors)


    def start(self):
        """Start the excursion.

        Raises:
            InvalidExhibitStateException: If already started, if there
                is no guide, or if the route is empty.
        """
        if self._is_started:
            raise InvalidExhibitStateException(
                exhibit_title=self._id,
                state="started",
                reason="Excursion has already started",
            )
        if self._guide is None:
            raise InvalidExhibitStateException(
                exhibit_title=self._id,
                state="no_guide",
                reason="Cannot start an excursion without a guide",
            )
        if not self._route_points:
            raise InvalidExhibitStateException(
                exhibit_title=self._id,
                state="empty_route",
                reason="Cannot start an excursion with an empty route",
            )
        self._is_started = True
        return True

    def finish(self):
        """Finish the excursion.

        Raises:
            InvalidExhibitStateException: If not started or already
                finished.
        """
        if not self._is_started:
            raise InvalidExhibitStateException(
                exhibit_title=self._id,
                state="not_started",
                reason="Cannot finish an excursion that has not started",
            )
        if self._is_finished:
            raise InvalidExhibitStateException(
                exhibit_title=self._id,
                state="finished",
                reason="Excursion has already finished",
            )
        self._is_finished = True
        return True

    def change_guide(self, new_guide):
        """Replace the tour guide.

        Only allowed before the tour starts.

        Args:
            new_guide: The new guide. Must not be None.

        Raises:
            ValueError: If new_guide is None.
            InvalidExhibitStateException: If the tour has already started.
        """
        if new_guide is None:
            raise ValueError("Guide must not be None")
        if self._is_started:
            raise InvalidExhibitStateException(
                exhibit_title=self._id,
                state="started",
                reason="Cannot change guide after the tour has started",
            )
        self._guide = new_guide
        return True