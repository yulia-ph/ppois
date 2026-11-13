from datetime import date

import pytest

from exceptions.InvalidCargoStateException import InvalidCargoStateException
from logistics_fleet.MaintenanceRecord import MaintenanceRecord
from logistics_people.Mechanic import Mechanic


class TestMaintenanceRecord:
    def test_maintenance(self, truck):
        mech = Mechanic("Kozlov", 40_000, date(2019, 1, 1), "engine", "CERT-1")
        rec = MaintenanceRecord(truck, mech, "oil", 100)
        rec.start_work()
        rec.add_part("filter", 20)
        assert rec.estimate_downtime() >= 2
        rec.complete()
        assert rec.status == MaintenanceRecord.STATUS_DONE
        with pytest.raises(InvalidCargoStateException):
            rec.add_part("x", 1)

    def test_maintenance_errors(self, truck):
        mech = Mechanic("K", 1, date(2019, 1, 1), "e", "c")
        with pytest.raises(ValueError):
            MaintenanceRecord(None, mech, "d", 1)
        with pytest.raises(ValueError):
            MaintenanceRecord(truck, None, "d", 1)
        with pytest.raises(ValueError):
            MaintenanceRecord(truck, mech, "", 1)
        with pytest.raises(ValueError):
            MaintenanceRecord(truck, mech, "d", -1)
        rec = MaintenanceRecord(truck, mech, "d", 1)
        with pytest.raises(InvalidCargoStateException):
            rec.complete()
        rec.start_work()
        with pytest.raises(InvalidCargoStateException):
            rec.start_work()
        with pytest.raises(ValueError):
            rec.add_part("", 1)
        with pytest.raises(ValueError):
            rec.add_part("p", -1)
