from exceptions.RouteConflictException import RouteConflictException


class TrackingSystem:
    """Tracks live trips and last known positions."""

    AVERAGE_SPEED_KMH = 60.0

    def __init__(self):
        self._trips = []
        self._last_positions = {}

    @property
    def trips(self):
        return list(self._trips)

    @property
    def last_positions(self):
        return dict(self._last_positions)

    def register_trip(self, trip):
        """Register a trip. A vehicle cannot have two running trips."""
        if trip is None:
            raise ValueError("Trip must not be None")
        for existing in self._trips:
            if existing.vehicle is trip.vehicle and existing.status in ("running", "paused"):
                raise RouteConflictException(
                    reason=f"Vehicle {trip.vehicle.plate} is already tracked",
                )
        self._trips.append(trip)
        return True

    def update_position(self, trip, gps):
        """Store the last GPS for a registered trip."""
        if trip not in self._trips:
            raise ValueError("Trip is not registered")
        if gps is None:
            raise ValueError("GPS position must not be None")
        self._last_positions[trip.vehicle.plate] = gps
        trip.vehicle.locate(gps)
        return True

    def find_vehicle(self, plate: str):
        """Return the trip for a plate, or None."""
        if not plate:
            raise ValueError("Plate must not be empty")
        for trip in self._trips:
            if trip.vehicle.plate == plate:
                return trip
        return None

    def eta(self, trip) -> float:
        """Hours remaining at AVERAGE_SPEED_KMH, plus delay."""
        if trip not in self._trips:
            raise ValueError("Trip is not registered")
        remaining_km = trip.route.distance_km
        hours = remaining_km / TrackingSystem.AVERAGE_SPEED_KMH
        return hours + trip._delay_minutes / 60.0
