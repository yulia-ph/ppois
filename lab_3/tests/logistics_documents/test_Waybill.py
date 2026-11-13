import pytest

from exceptions.InvalidCargoStateException import InvalidCargoStateException
from logistics_documents.Waybill import Waybill
from logistics_orders.ShipmentOrder import ShipmentOrder
from logistics_people.Client import Client
from logistics_people.Consignee import Consignee


class TestWaybill:
    def test_waybill(self, cargo, route, address):
        client = Client("A", "T", 1)
        order = ShipmentOrder(client, cargo, route, 1)
        cons = Consignee("Shop", address, "123")
        wb = Waybill(order, "BelLogistic", cons, "boxes")
        wb.issue()
        wb.sign_by_driver()
        wb.sign_by_consignee()
        assert wb.is_signed
        wb2 = Waybill(order, "S", cons, "boxes")
        wb2.issue()
        wb2.cancel()
        with pytest.raises(ValueError):
            Waybill(None, "s", cons, "c")
        with pytest.raises(ValueError):
            Waybill(order, "", cons, "c")
        with pytest.raises(ValueError):
            Waybill(order, "s", cons, "")
        with pytest.raises(InvalidCargoStateException):
            wb.issue()
        fresh = Waybill(order, "s", cons, "c")
        with pytest.raises(InvalidCargoStateException):
            fresh.sign_by_driver()
        with pytest.raises(InvalidCargoStateException):
            fresh.sign_by_consignee()
        with pytest.raises(InvalidCargoStateException):
            wb.cancel()
