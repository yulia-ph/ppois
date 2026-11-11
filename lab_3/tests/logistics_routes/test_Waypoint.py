from datetime import timedelta

import pytest

from exceptions.InvalidCargoStateException import InvalidCargoStateException
from logistics_routes.Waypoint import Waypoint


class TestWaypoint:
    def test_waypoint(self, address, now_window):
        start, end = now_window
        wp = Waypoint(address, 1, start, end, Waypoint.STOP_DELIVERY)
        wp.arrive()
        wp.depart()
        assert wp.is_visited
        assert not wp.is_missed()
        wp2 = Waypoint(address, 2, start - timedelta(days=2), start - timedelta(days=1), Waypoint.STOP_REST)
        assert wp2.is_missed()
        wp2.reschedule(start, end)
        with pytest.raises(ValueError):
            Waypoint(None, 1, start, end, Waypoint.STOP_PICKUP)
        with pytest.raises(ValueError):
            Waypoint(address, 0, start, end, Waypoint.STOP_PICKUP)
        with pytest.raises(ValueError):
            Waypoint(address, 1, end, start, Waypoint.STOP_PICKUP)
        with pytest.raises(ValueError):
            Waypoint(address, 1, start, end, "x")
        with pytest.raises(InvalidCargoStateException):
            wp.arrive()
        wp3 = Waypoint(address, 3, start, end, Waypoint.STOP_PICKUP)
        with pytest.raises(InvalidCargoStateException):
            wp3.depart()
        with pytest.raises(InvalidCargoStateException):
            wp.reschedule(start, end)
        with pytest.raises(ValueError):
            wp3.reschedule(end, start)
