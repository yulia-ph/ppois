
import pytest

from logistics_routes.TrackingEvent import TrackingEvent
from logistics_routes.Trip import Trip


class TestTrackingEvent:
    def test_record_and_describe(self, truck, driver, route, gps):
        truck.assign_driver(driver)
        trip = Trip(truck, driver, route)
        trip.start()
        ev = TrackingEvent(trip, gps, TrackingEvent.TYPE_POSITION)
        ev.record()
        assert not ev.is_delay()
        assert "position" in ev.describe()
        delay = TrackingEvent(trip, gps, TrackingEvent.TYPE_DELAY)
        assert delay.is_delay()

    def test_errors(self, truck, driver, route, gps):
        trip = Trip(truck, driver, route)
        with pytest.raises(ValueError):
            TrackingEvent(None, gps, TrackingEvent.TYPE_ARRIVAL)
        with pytest.raises(ValueError):
            TrackingEvent(trip, None, TrackingEvent.TYPE_ARRIVAL)
        with pytest.raises(ValueError):
            TrackingEvent(trip, gps, "x")
