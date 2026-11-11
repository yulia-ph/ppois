import pytest

from exceptions.InvalidCargoStateException import InvalidCargoStateException
from logistics_documents.CargoManifest import CargoManifest
from logistics_orders.ShipmentOrder import ShipmentOrder
from logistics_people.Client import Client


class TestCargoManifest:
    def test_manifest(self, cargo, route):
        client = Client("A", "T", 1)
        order = ShipmentOrder(client, cargo, route, 1)
        m = CargoManifest(order, "clerk")
        m.add_item(cargo)
        assert m.total_weight() == cargo.weight
        m.verify()
        with pytest.raises(ValueError):
            CargoManifest(None, "i")
        with pytest.raises(ValueError):
            CargoManifest(order, "")
        m2 = CargoManifest(order, "i")
        with pytest.raises(ValueError):
            m2.add_item(None)
        with pytest.raises(ValueError):
            m2.verify()
        m2.add_item(cargo)
        m2.remove_item(cargo)
        with pytest.raises(ValueError):
            m2.remove_item(cargo)
        m2.add_item(cargo)
        m2.verify()
        with pytest.raises(InvalidCargoStateException):
            m2.add_item(cargo)
        with pytest.raises(InvalidCargoStateException):
            m2.remove_item(cargo)
        with pytest.raises(InvalidCargoStateException):
            m2.verify()
