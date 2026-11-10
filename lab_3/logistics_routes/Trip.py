from datetime import datetime

from exceptions.InvalidCargoStateException import InvalidCargoStateException
from exceptions.RouteConflictException import RouteConflictException


class Trip:
    """A vehicle/driver run along a route."""

    STATUS_PLANNED = "planned"
    STATUS_RUNNING = "running"
    STATUS_PAUSED = "paused"
    STATUS_FINISHED = "finished"

    def __init__(self, vehicle, driver, route):
        if vehicle is None or driver is None or route is None:
            raise ValueError("Vehicle, driver and route must not be None")
        self._vehicle = vehicle
        self._driver = driver
        self._route = route
        self._started_at = None
        self._finished_at = None
        self._status = Trip.STATUS_PLANNED
        self._delay_minutes = 0

    @property
    def vehicle(self):
        return self._vehicle

    @property
    def driver(self):
        return self._driver

    @property
    def route(self):
        return self._route

    @property
    def started_at(self):
        return self._started_at

    @property
    def finished_at(self):
        return self._finished_at

    @property
    def status(self):
        return self._status

    def start(self):
        """Start the trip and the vehicle."""
        if self._status != Trip.STATUS_PLANNED:
            raise RouteConflictException(reason="Trip already started")
        if self._vehicle.status == "on_trip":
            raise RouteConflictException(reason="Vehicle is already on another trip")
        self._vehicle.start_trip()
        self._started_at = datetime.now()
        self._status = Trip.STATUS_RUNNING
        return True

    def pause(self):
        """Pause a running trip."""
        if self._status != Trip.STATUS_RUNNING:
            raise InvalidCargoStateException(
                title=self._vehicle.plate,
                state=self._status,
                reason="Trip is not running",
            )
        self._status = Trip.STATUS_PAUSED
        return True

    def resume(self):
        """Resume a paused trip."""
        if self._status != Trip.STATUS_PAUSED:
            raise InvalidCargoStateException(
                title=self._vehicle.plate,
                state=self._status,
                reason="Trip is not paused",
            )
        self._status = Trip.STATUS_RUNNING
        return True

    def add_delay(self, minutes: int):
        """Add delay minutes to a running or paused trip."""
        if minutes <= 0:
            raise ValueError(f"Minutes must be positive, got {minutes}")
        if self._status not in (Trip.STATUS_RUNNING, Trip.STATUS_PAUSED):
            raise InvalidCargoStateException(
                title=self._vehicle.plate,
                state=self._status,
                reason="Cannot delay a trip that is not underway",
            )
        self._delay_minutes += minutes
        return True

    def finish(self):
        """Finish the trip."""
        if self._status not in (Trip.STATUS_RUNNING, Trip.STATUS_PAUSED):
            raise InvalidCargoStateException(
                title=self._vehicle.plate,
                state=self._status,
                reason="Trip is not underway",
            )
        self._vehicle.finish_trip(self._route.distance_km)
        self._finished_at = datetime.now()
        self._status = Trip.STATUS_FINISHED
        return True
