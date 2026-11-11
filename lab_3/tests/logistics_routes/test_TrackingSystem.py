import pytest

from exceptions.RouteConflictException import RouteConflictException
from logistics_routes.TrackingEvent import TrackingEvent
from logistics_routes.TrackingSystem import TrackingSystem
from logistics_routes.Trip import Trip


class TestTrackingSystem:
    def test_tracking(self, truck, driver, route, gps):
        truck.assign_driver(driver)
        trip = Trip(truck, driver, route)
        trip.start()
        sys = TrackingSystem()
        sys.register_trip(trip)
        sys.update_position(trip, gps)
        ev = TrackingEvent(trip, gps, TrackingEvent.TYPE_POSITION)
        ev.record()
        assert not ev.is_delay()
        assert "position" in ev.describe()
        delay = TrackingEvent(trip, gps, TrackingEvent.TYPE_DELAY)
        assert delay.is_delay()
        assert sys.find_vehicle(truck.plate) is trip
        assert sys.find_vehicle("NO") is None
        assert sys.eta(trip) > 0
        with pytest.raises(RouteConflictException):
            sys.register_trip(trip)
        # second running trip same vehicle
        trip.pause()
        other = Trip(truck, driver, route)
        # trip still paused so still conflict
        with pytest.raises(RouteConflictException):
            sys.register_trip(other)

    def test_tracking_errors(self, truck, driver, route, gps):
        trip = Trip(truck, driver, route)
        sys = TrackingSystem()
        with pytest.raises(ValueError):
            sys.register_trip(None)
        with pytest.raises(ValueError):
            sys.update_position(trip, gps)
        sys.register_trip(trip)
        with pytest.raises(ValueError):
            sys.update_position(trip, None)
        with pytest.raises(ValueError):
            sys.find_vehicle("")
        with pytest.raises(ValueError):
            sys.eta(Trip(truck, driver, route))
        with pytest.raises(ValueError):
            TrackingEvent(None, gps, TrackingEvent.TYPE_ARRIVAL)
        with pytest.raises(ValueError):
            TrackingEvent(trip, None, TrackingEvent.TYPE_ARRIVAL)
        with pytest.raises(ValueError):
            TrackingEvent(trip, gps, "x")
