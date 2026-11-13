import pytest

from exceptions.InvalidCargoStateException import InvalidCargoStateException
from logistics_documents.Claim import Claim
from logistics_orders.ShipmentOrder import ShipmentOrder
from logistics_people.Client import Client


class TestClaim:
    def test_claim(self, cargo, route):
        client = Client("A", "T", 1)
        order = ShipmentOrder(client, cargo, route, 1)
        claim = Claim(order, "broken", 50)
        claim.file()
        claim.add_evidence("photo")
        claim.approve()
        c2 = Claim(order, "late", 10)
        c2.file()
        c2.reject()
        with pytest.raises(ValueError):
            Claim(None, "r", 1)
        with pytest.raises(ValueError):
            Claim(order, "", 1)
        with pytest.raises(ValueError):
            Claim(order, "r", 0)
        c3 = Claim(order, "r", 1)
        with pytest.raises(InvalidCargoStateException):
            c3.add_evidence("x")
        with pytest.raises(InvalidCargoStateException):
            c3.approve()
        with pytest.raises(InvalidCargoStateException):
            c3.reject()
        c3.file()
        with pytest.raises(InvalidCargoStateException):
            c3.file()
        with pytest.raises(ValueError):
            c3.add_evidence("")
