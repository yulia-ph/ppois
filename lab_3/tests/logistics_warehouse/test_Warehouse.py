import pytest

from exceptions.WarehouseCapacityExceededException import WarehouseCapacityExceededException
from logistics_cargo.Cargo import Cargo
from logistics_warehouse.StorageZone import StorageZone
from logistics_warehouse.Warehouse import Warehouse


class TestWarehouse:
    def test_receive_ship_inventory(self, warehouse, cargo, address, address_warsaw):
        warehouse.receive(cargo)
        assert warehouse.find_cargo(cargo.tracking_id) is cargo
        result = warehouse.run_inventory([cargo])
        assert result["is_clean"]
        warehouse.ship(cargo)
        with pytest.raises(WarehouseCapacityExceededException):
            big = Cargo(1, 5000, address, address_warsaw)
            warehouse.receive(big)

    def test_warehouse_errors(self, address, cargo):
        with pytest.raises(ValueError):
            Warehouse("", address, 1)
        with pytest.raises(ValueError):
            Warehouse("w", None, 1)
        with pytest.raises(ValueError):
            Warehouse("w", address, 0)
        w = Warehouse("w", address, 10)
        with pytest.raises(ValueError):
            w.add_zone(None)
        z = StorageZone("z", w, StorageZone.TYPE_AMBIENT, 10)
        w.add_zone(z)
        with pytest.raises(ValueError):
            w.add_zone(z)
        with pytest.raises(ValueError):
            w.receive(None)
        w.receive(cargo)
        with pytest.raises(ValueError):
            w.receive(cargo)
        with pytest.raises(ValueError):
            w.ship(object())
        with pytest.raises(ValueError):
            w.find_cargo("nope")
        with pytest.raises(ValueError):
            w.run_inventory(None)
        extra = w.run_inventory([])
        assert extra["extra"]
