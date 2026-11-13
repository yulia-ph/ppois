import pytest

from exceptions.InvalidCargoStateException import InvalidCargoStateException
from logistics_documents.Incident import Incident
from logistics_orders.ShipmentOrder import ShipmentOrder
from logistics_people.Client import Client


class TestIncident:
    def test_incident(self, truck, driver, cargo, route):
        inc = Incident(Incident.TYPE_ACCIDENT, "M1", 3, truck, driver)
        inc.add_evidence("photo")
        client = Client("A", "T", 1)
        order = ShipmentOrder(client, cargo, route, 1)
        inc.link_order(order)
        assert inc.is_open()
        inc.close()
        with pytest.raises(InvalidCargoStateException):
            inc.add_evidence("x")
        with pytest.raises(ValueError):
            Incident("x", "p", 1, truck, driver)
        with pytest.raises(ValueError):
            Incident(Incident.TYPE_THEFT, "", 1, truck, driver)
        with pytest.raises(ValueError):
            Incident(Incident.TYPE_BREAKDOWN, "p", 9, truck, driver)
        with pytest.raises(ValueError):
            Incident(Incident.TYPE_ACCIDENT, "p", 1, None, driver)
        with pytest.raises(ValueError):
            inc.add_evidence("")
        with pytest.raises(InvalidCargoStateException):
            inc.close()
        with pytest.raises(ValueError):
            inc.link_order(None)
