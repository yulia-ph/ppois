import pytest

from exceptions.InsufficientFundsException import InsufficientFundsException
from exceptions.OrderNotFoundException import OrderNotFoundException
from logistics_core.TransportCompany import TransportCompany
from logistics_fleet.Truck import Truck
from logistics_orders.ShipmentOrder import ShipmentOrder
from logistics_people.Client import Client


class TestTransportCompany:
    def test_budget_and_collections(self, company, truck, warehouse, employee, address):
        company.add_vehicle(truck)
        company.add_warehouse(warehouse)
        company.add_employee(employee)
        client = Client("Acme", "TAX1", 10_000)
        company.register_client(client)
        assert company.find_vehicle("AA-1234") is truck
        company.spend_budget(1000)
        assert company.budget == 99_000
        company.increase_budget(500)
        assert company.budget == 99_500
        company.remove_vehicle(truck)
        with pytest.raises(ValueError):
            company.find_vehicle("AA-1234")

    def test_insufficient(self, company):
        with pytest.raises(InsufficientFundsException):
            company.spend_budget(999_999)

    def test_order_lookup(self, company, cargo, route, address):
        client = Client("Acme", "TAX1", 10_000)
        order = ShipmentOrder(client, cargo, route, 100)
        company.register_order(order)
        assert company.find_order(order.number) is order
        with pytest.raises(OrderNotFoundException):
            company.find_order("NOPE")

    def test_validation(self, address, truck, warehouse, employee):
        with pytest.raises(ValueError):
            TransportCompany("", "L", address)
        with pytest.raises(ValueError):
            TransportCompany("C", "", address)
        with pytest.raises(ValueError):
            TransportCompany("C", "L", None)
        c = TransportCompany("C", "L", address)
        with pytest.raises(ValueError):
            c.add_vehicle(None)
        c.add_vehicle(truck)
        with pytest.raises(ValueError):
            c.add_vehicle(truck)
        with pytest.raises(ValueError):
            c.remove_vehicle(Truck("X", "Y", 1, 1, 2))
        with pytest.raises(ValueError):
            c.add_warehouse(None)
        c.add_warehouse(warehouse)
        with pytest.raises(ValueError):
            c.add_warehouse(warehouse)
        with pytest.raises(ValueError):
            c.add_employee(None)
        c.add_employee(employee)
        with pytest.raises(ValueError):
            c.add_employee(employee)
        with pytest.raises(ValueError):
            c.register_client(None)
        cl = Client("A", "T", 1)
        c.register_client(cl)
        with pytest.raises(ValueError):
            c.register_client(cl)
        with pytest.raises(ValueError):
            c.register_order(None)
        with pytest.raises(ValueError):
            c.find_vehicle("")
        with pytest.raises(ValueError):
            c.find_order("")
        with pytest.raises(ValueError):
            c.set_budget(-1)
        with pytest.raises(ValueError):
            c.increase_budget(0)
        with pytest.raises(ValueError):
            c.spend_budget(0)
        c.set_budget(10)
        assert c.license_number == "L"
