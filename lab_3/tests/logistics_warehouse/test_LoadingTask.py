from datetime import datetime, timedelta

import pytest

from exceptions.InvalidCargoStateException import InvalidCargoStateException
from logistics_core.Dock import Dock
from logistics_orders.ShipmentOrder import ShipmentOrder
from logistics_people.Client import Client
from logistics_warehouse.LoadingTask import LoadingTask


class TestLoadingTask:
    def test_loading_task(self, cargo, route, employee, warehouse):
        dock = Dock(1, 20)
        client = Client("A", "T", 1)
        order = ShipmentOrder(client, cargo, route, 1)
        task = LoadingTask(dock, order, employee)
        task.assign_worker(employee)
        task.start()
        assert not task.is_overdue(limit_minutes=60)
        assert task.is_overdue(limit_minutes=0, now=datetime.now() + timedelta(minutes=1))
        task.finish()
        with pytest.raises(ValueError):
            LoadingTask(None, order, employee)
        t2 = LoadingTask(dock, order, employee)
        with pytest.raises(ValueError):
            t2.assign_worker(None)
        t2.start()
        with pytest.raises(InvalidCargoStateException):
            t2.assign_worker(employee)
        with pytest.raises(InvalidCargoStateException):
            t2.start()
        open_task = LoadingTask(dock, order, employee)
        with pytest.raises(InvalidCargoStateException):
            open_task.finish()
        assert not open_task.is_overdue()
