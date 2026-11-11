import pytest

from logistics_routes.Route import Route
from logistics_routes.Waypoint import Waypoint


class TestRoute:
    def test_route(self, address, address_warsaw, now_window):
        route = Route(address, address_warsaw, 500, 7)
        start, end = now_window
        wp = Waypoint(address, 1, start, end, Waypoint.STOP_PICKUP)
        route.add_waypoint(wp)
        assert route.crosses_border()
        assert route.total_distance() == 510
        assert route.duration() == 7.5
        route.remove_waypoint(wp)
        with pytest.raises(ValueError):
            Route(None, address_warsaw, 1, 1)
        with pytest.raises(ValueError):
            Route(address, address_warsaw, 0, 1)
        with pytest.raises(ValueError):
            Route(address, address_warsaw, 1, 0)
        with pytest.raises(ValueError):
            route.add_waypoint(None)
        route.add_waypoint(wp)
        with pytest.raises(ValueError):
            route.add_waypoint(wp)
        with pytest.raises(ValueError):
            route.remove_waypoint(Waypoint(address, 9, start, end, Waypoint.STOP_REST))

    def test_same_country_no_border(self, address):
        other = address.__class__("x", "Grodno", "G", "Belarus", "1")
        r = Route(address, other, 10, 1)
        assert not r.crosses_border()
