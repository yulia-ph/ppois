from datetime import date

import pytest

from exceptions.InvalidCargoStateException import InvalidCargoStateException
from logistics_people.WarehouseWorker import WarehouseWorker


class TestWarehouseWorker:
    def test_warehouse_worker(self, warehouse, cargo, employee):
        from logistics_warehouse.StorageZone import StorageZone
        zone = StorageZone("Z", warehouse, StorageZone.TYPE_AMBIENT, 18)
        worker = WarehouseWorker("W", 30_000, date(2022, 1, 1), warehouse, True)
        worker.put_away(cargo)
        assert worker.count_items() == 1
        worker.operate_forklift(zone)
        worker.pick_item(cargo)
        w2 = WarehouseWorker("W2", 1, date.today(), warehouse, False)
        with pytest.raises(InvalidCargoStateException):
            w2.operate_forklift(zone)
        with pytest.raises(ValueError):
            WarehouseWorker("n", 1, date.today(), None)
        with pytest.raises(ValueError):
            worker.pick_item(None)
        with pytest.raises(ValueError):
            worker.put_away(None)
        with pytest.raises(ValueError):
            worker.operate_forklift(None)
