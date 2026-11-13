import pytest

from exceptions.DeliveryRefusedException import DeliveryRefusedException
from exceptions.InvalidCargoStateException import InvalidCargoStateException
from logistics_orders.Delivery import Delivery
from logistics_orders.ShipmentOrder import ShipmentOrder
from logistics_people.Client import Client


class TestDelivery:
    def test_delivery(self, cargo, route, truck, driver):
        client = Client("A", "T", 1)
        order = ShipmentOrder(client, cargo, route, 1)
        order.confirm()
        truck.assign_driver(driver)
        order.assign_vehicle(truck)
        order.assign_driver(driver)
        order.dispatch()
        d = Delivery(order)
        d.mark_partial()
        d.attach_note("left at door")
        d.confirm("Ivan")
        with pytest.raises(InvalidCargoStateException):
            d.confirm("x")
        with pytest.raises(ValueError):
            Delivery(None)
        d2_order = ShipmentOrder(client, cargo, route, 1)
        d2_order.confirm()
        d2 = Delivery(d2_order)
        with pytest.raises(ValueError):
            d2.confirm("")
        with pytest.raises(ValueError):
            d2.refuse("")
        with pytest.raises(ValueError):
            d2.attach_note("")
        with pytest.raises(DeliveryRefusedException):
            d2.refuse("wet")
        with pytest.raises(InvalidCargoStateException):
            d2.confirm("x")
        d3 = Delivery(d2_order)
        d3.confirm("ok")
        with pytest.raises(InvalidCargoStateException):
            d3.mark_partial()
        with pytest.raises(InvalidCargoStateException):
            d3.refuse("late")
