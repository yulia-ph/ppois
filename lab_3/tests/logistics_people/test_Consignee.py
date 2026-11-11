from datetime import date, timedelta

import pytest

from logistics_orders.Delivery import Delivery
from logistics_orders.ShipmentOrder import ShipmentOrder
from logistics_people.Client import Client
from logistics_people.Consignee import Consignee
from logistics_people.Driver import Driver
from logistics_people.DrivingLicense import DrivingLicense


class TestConsignee:
    def test_consignee(self, address, cargo, route):
        cons = Consignee("Shop", address, "+375")
        client = Client("A", "T", 1)
        order = ShipmentOrder(client, cargo, route, 1)
        order.confirm()
        from logistics_fleet.Truck import Truck
        lic = DrivingLicense("x", ["C"], date(2020, 1, 1), date.today() + timedelta(days=10))
        drv = Driver("D", 1, date.today(), lic)
        truck = Truck("P", "V", 10000, 40, 3)
        truck.assign_driver(drv)
        order.assign_vehicle(truck)
        order.assign_driver(drv)
        order.dispatch()
        delivery = Delivery(order)
        cons.confirm_delivery(delivery)
        cons.reschedule("10:00-12:00")
        with pytest.raises(ValueError):
            Consignee("", address, "1")
        with pytest.raises(ValueError):
            Consignee("n", None, "1")
        with pytest.raises(ValueError):
            Consignee("n", address, "")
        with pytest.raises(ValueError):
            cons.confirm_delivery(None)
        with pytest.raises(ValueError):
            cons.refuse(None, "x")
        with pytest.raises(ValueError):
            cons.refuse(Delivery(order), "")
        with pytest.raises(ValueError):
            cons.reschedule("")
