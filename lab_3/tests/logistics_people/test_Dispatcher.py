from datetime import date

import pytest

from exceptions.DriverNotAvailableException import DriverNotAvailableException
from exceptions.OrderNotFoundException import OrderNotFoundException
from exceptions.VehicleNotAvailableException import VehicleNotAvailableException
from logistics_orders.ShipmentOrder import ShipmentOrder
from logistics_people.Client import Client
from logistics_people.Dispatcher import Dispatcher
from logistics_people.Driver import Driver


class TestDispatcher:
    def test_dispatcher(self, driver, truck, cargo, route):
        truck.assign_driver(driver)
        disp = Dispatcher("Sidorov", 55_000, date(2018, 1, 1), "west", "R-1")
        client = Client("Acme", "T", 10_000)
        order = ShipmentOrder(client, cargo, route, 100)
        order.confirm()
        found = disp.find_free_driver([driver])
        assert found is driver
        disp.assign_order(order, driver)
        d2 = Driver("Other", 1, date.today(), driver.license)
        truck2 = truck.__class__("BB-2", "VIN2", 10_000, 40, 3)
        truck2.assign_driver(d2)
        disp.reassign(order, d2)
        disp.close_shift()
        assert disp.assigned_orders == []

    def test_dispatcher_errors(self, driver, truck, cargo, route):
        with pytest.raises(ValueError):
            Dispatcher("n", 1, date.today(), "", "r")
        with pytest.raises(ValueError):
            Dispatcher("n", 1, date.today(), "r", "")
        disp = Dispatcher("n", 1, date.today(), "r", "id")
        with pytest.raises(ValueError):
            disp.find_free_driver(None)
        with pytest.raises(DriverNotAvailableException):
            disp.find_free_driver([])
        with pytest.raises(ValueError):
            disp.assign_order(None, driver)
        client = Client("A", "T", 1)
        order = ShipmentOrder(client, cargo, route, 1)
        order.confirm()
        with pytest.raises(VehicleNotAvailableException):
            disp.assign_order(order, driver)
        with pytest.raises(OrderNotFoundException):
            disp.reassign(order, driver)
