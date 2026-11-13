class Route:
    """Origin, destination and waypoints."""

    def __init__(self, origin, destination, distance_km: float, estimated_hours: float):
        if origin is None or destination is None:
            raise ValueError("Origin and destination must not be None")
        if distance_km <= 0:
            raise ValueError(f"Distance must be positive, got {distance_km}")
        if estimated_hours <= 0:
            raise ValueError(f"Estimated hours must be positive, got {estimated_hours}")
        self._origin = origin
        self._destination = destination
        self._waypoints = []
        self._distance_km = distance_km
        self._estimated_hours = estimated_hours

    @property
    def origin(self):
        return self._origin

    @property
    def destination(self):
        return self._destination

    @property
    def waypoints(self):
        return list(self._waypoints)

    @property
    def distance_km(self):
        return self._distance_km

    @property
    def estimated_hours(self):
        return self._estimated_hours

    def add_waypoint(self, waypoint):
        """Append a waypoint."""
        if waypoint is None:
            raise ValueError("Waypoint must not be None")
        if waypoint in self._waypoints:
            raise ValueError("Waypoint is already on this route")
        self._waypoints.append(waypoint)
        return True

    def remove_waypoint(self, waypoint):
        """Remove a waypoint."""
        if waypoint not in self._waypoints:
            raise ValueError("Waypoint is not on this route")
        self._waypoints.remove(waypoint)
        return True

    def duration(self) -> float:
        """Estimated hours, plus 0.5 h per waypoint."""
        return self._estimated_hours + 0.5 * len(self._waypoints)

    def crosses_border(self) -> bool:
        """True if origin and destination are in different countries."""
        return self._origin.country.lower() != self._destination.country.lower()

    def total_distance(self) -> float:
        """Distance including 10 km per extra waypoint."""
        return self._distance_km + 10.0 * len(self._waypoints)
