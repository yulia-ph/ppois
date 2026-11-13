import pytest

from exceptions.InvalidCargoStateException import InvalidCargoStateException
from logistics_warehouse.InventoryCount import InventoryCount


class TestInventoryCount:
    def test_inventory_count(self, warehouse, cargo, employee):
        warehouse.receive(cargo)
        inv = InventoryCount(warehouse, employee)
        inv.scan(cargo)
        inv.reconcile(warehouse.find_cargo())
        assert inv.is_clean()
        report = inv.generate_report()
        assert report.data["scanned"] == 1
        missing, _extra = InventoryCount.diff([], [cargo])
        assert cargo in missing

    def test_inventory_errors(self, warehouse, cargo, employee):
        with pytest.raises(ValueError):
            InventoryCount(None, employee)
        with pytest.raises(ValueError):
            InventoryCount(warehouse, None)
        inv = InventoryCount(warehouse, employee)
        assert not inv.is_clean()
        with pytest.raises(ValueError):
            inv.scan(None)
        inv.scan(cargo)
        with pytest.raises(ValueError):
            inv.scan(cargo)
        with pytest.raises(ValueError):
            inv.reconcile(None)
        inv.reconcile([])
        with pytest.raises(InvalidCargoStateException):
            inv.reconcile([])
