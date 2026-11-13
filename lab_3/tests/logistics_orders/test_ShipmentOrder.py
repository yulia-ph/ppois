import pytest

from exceptions.InvalidCargoStateException import InvalidCargoStateException
from logistics_orders.ShipmentOrder import ShipmentOrder
from logistics_people.Client import Client


class TestShipmentOrder:
    def test_order_lifecycle(self, cargo, route, truck, driver):
        client = Client("A", "T", 1)
        order = ShipmentOrder(client, cargo, route, 200)
        order.confirm()
        truck.assign_driver(driver)
        order.assign_vehicle(truck)
        order.assign_driver(driver)
        order.dispatch()
        order.deliver()
        assert order.status == ShipmentOrder.STATUS_DELIVERED

    def test_order_cancel_and_errors(self, cargo, route, truck):
        client = Client("A", "T", 1)
        order = ShipmentOrder(client, cargo, route, 1)
        order.cancel()
        with pytest.raises(InvalidCargoStateException):
            order.confirm()
        o = ShipmentOrder(client, cargo, route, 1)
        with pytest.raises(InvalidCargoStateException):
            o.assign_vehicle(truck)
        with pytest.raises(InvalidCargoStateException):
            o.dispatch()
        o.confirm()
        with pytest.raises(InvalidCargoStateException):
            o.dispatch()
        with pytest.raises(InvalidCargoStateException):
            o.deliver()
        o.cancel()
        with pytest.raises(ValueError):
            ShipmentOrder(None, cargo, route, 1)
        with pytest.raises(ValueError):
            ShipmentOrder(client, cargo, route, -1)

    def test_assign_none(self, cargo, route):
        client = Client("A", "T", 1)
        o = ShipmentOrder(client, cargo, route, 1)
        o.confirm()
        with pytest.raises(ValueError):
            o.assign_vehicle(None)
        with pytest.raises(ValueError):
            o.assign_driver(None)
