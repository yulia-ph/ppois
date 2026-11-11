from datetime import date

import pytest

from exceptions.InvalidCargoStateException import InvalidCargoStateException
from logistics_people.WarehouseWorker import WarehouseWorker
from logistics_warehouse.StockMove import StockMove
from logistics_warehouse.StorageZone import StorageZone


class TestStockMove:
    def test_stock_move(self, warehouse, cargo, employee):
        z1 = StorageZone("A", warehouse, StorageZone.TYPE_AMBIENT, 18)
        z2 = StorageZone("B", warehouse, StorageZone.TYPE_COLD, 4)
        worker = WarehouseWorker("W", 1, date.today(), warehouse, True)
        move = StockMove(cargo, z1, z2, worker)
        move.register()
        move.confirm()
        move2 = StockMove(cargo, z1, z2, worker)
        move2.register()
        move2.cancel()
        with pytest.raises(ValueError):
            StockMove(None, z1, z2, worker)
        with pytest.raises(ValueError):
            StockMove(cargo, z1, z1, worker)
        with pytest.raises(InvalidCargoStateException):
            move.confirm()
        fresh = StockMove(cargo, z1, z2, worker)
        with pytest.raises(InvalidCargoStateException):
            fresh.confirm()
        fresh.register()
        with pytest.raises(InvalidCargoStateException):
            fresh.register()
        with pytest.raises(InvalidCargoStateException):
            move.cancel()
