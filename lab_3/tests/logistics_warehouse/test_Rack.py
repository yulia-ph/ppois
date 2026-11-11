import pytest

from exceptions.InvalidCargoStateException import InvalidCargoStateException
from logistics_warehouse.Rack import Rack
from logistics_warehouse.StorageZone import StorageZone


class TestRack:
    def test_zone_rack_errors(self, warehouse, cargo):
        with pytest.raises(ValueError):
            StorageZone("", warehouse, StorageZone.TYPE_AMBIENT, 1)
        with pytest.raises(ValueError):
            StorageZone("z", None, StorageZone.TYPE_AMBIENT, 1)
        with pytest.raises(ValueError):
            StorageZone("z", warehouse, "x", 1)
        z = StorageZone("z", warehouse, StorageZone.TYPE_HAZMAT, 1)
        with pytest.raises(ValueError):
            z.add_rack(None)
        rack = Rack("r", z, 1, 500)
        z.add_rack(rack)
        with pytest.raises(ValueError):
            z.add_rack(rack)
        with pytest.raises(ValueError):
            Rack("", z, 1, 1)
        with pytest.raises(ValueError):
            Rack("r", None, 1, 1)
        with pytest.raises(ValueError):
            Rack("r", z, 0, 1)
        with pytest.raises(ValueError):
            Rack("r", z, 1, 0)
        with pytest.raises(ValueError):
            rack.place(None)
        tiny = Rack("t", z, 1, 0.01)
        with pytest.raises(InvalidCargoStateException):
            tiny.place(cargo)
        rack.place(cargo)
        with pytest.raises(InvalidCargoStateException):
            rack.place(cargo)
        with pytest.raises(ValueError):
            rack.remove(object())
