from datetime import timedelta

import pytest

from exceptions.InvalidCargoStateException import InvalidCargoStateException
from logistics_orders.Pickup import Pickup
from logistics_orders.ShipmentOrder import ShipmentOrder
from logistics_people.Client import Client


class TestPickup:
    def test_pickup(self, cargo, route, warehouse, now_window):
        client = Client("A", "T", 1)
        order = ShipmentOrder(client, cargo, route, 1)
        start, end = now_window
        p = Pickup(order, warehouse, start, end)
        p.schedule(start + timedelta(hours=1), end + timedelta(hours=1))
        warehouse.receive(cargo)
        p.complete()
        p2 = Pickup(order, warehouse, start, end)
        p2.fail("no show")
        with pytest.raises(ValueError):
            Pickup(None, warehouse, start, end)
        with pytest.raises(ValueError):
            Pickup(order, warehouse, end, start)
        with pytest.raises(InvalidCargoStateException):
            p.complete()
        with pytest.raises(InvalidCargoStateException):
            p2.reschedule(start, end)
        with pytest.raises(ValueError):
            Pickup(order, warehouse, start, end).reschedule(end, start)
        with pytest.raises(ValueError):
            Pickup(order, warehouse, start, end).fail("")
        done = Pickup(order, warehouse, start, end)
        done.complete()
        with pytest.raises(InvalidCargoStateException):
            done.fail("x")
