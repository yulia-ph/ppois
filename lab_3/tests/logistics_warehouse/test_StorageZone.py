import pytest

from exceptions.InvalidCargoStateException import InvalidCargoStateException
from logistics_warehouse.Rack import Rack
from logistics_warehouse.StorageZone import StorageZone


class TestStorageZone:
    def test_zone_rack(self, warehouse, cargo):
        zone = StorageZone("Cold", warehouse, StorageZone.TYPE_COLD, 4)
        warehouse.add_zone(zone)
        rack = Rack("R1", zone, 5, 500)
        zone.add_rack(rack)
        rack.place(cargo)
        rack.remove(cargo)
        assert zone.check_temperature(4)
        zone.lock()
        with pytest.raises(InvalidCargoStateException):
            zone.check_temperature(4)
        zone.unlock()
