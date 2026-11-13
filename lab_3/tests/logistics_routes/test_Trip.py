import pytest

from exceptions.InvalidCargoStateException import InvalidCargoStateException
from exceptions.RouteConflictException import RouteConflictException
from logistics_routes.Trip import Trip


class TestTrip:
    def test_trip(self, truck, driver, route):
        truck.assign_driver(driver)
        trip = Trip(truck, driver, route)
        trip.start()
        trip.pause()
        trip.resume()
        trip.add_delay(15)
        trip.finish()
        assert trip.status == Trip.STATUS_FINISHED

    def test_trip_errors(self, truck, driver, route):
        with pytest.raises(ValueError):
            Trip(None, driver, route)
        trip = Trip(truck, driver, route)
        with pytest.raises(InvalidCargoStateException):
            trip.pause()
        with pytest.raises(InvalidCargoStateException):
            trip.resume()
        with pytest.raises(InvalidCargoStateException):
            trip.add_delay(1)
        with pytest.raises(InvalidCargoStateException):
            trip.finish()
        trip.start()
        with pytest.raises(RouteConflictException):
            trip.start()
        with pytest.raises(ValueError):
            trip.add_delay(0)
        trip2 = Trip(truck, driver, route)
        with pytest.raises(RouteConflictException):
            trip2.start()
        trip.pause()
        with pytest.raises(InvalidCargoStateException):
            trip.pause()
