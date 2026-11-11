from datetime import date

import pytest

from logistics_fleet.MaintenanceRecord import MaintenanceRecord
from logistics_people.Mechanic import Mechanic


class TestMechanic:
    def test_mechanic(self, truck):
        m = Mechanic("M", 1, date.today(), "engine", "C1")
        rec = MaintenanceRecord(truck, m, "fix", 10)
        m.repair(rec)
        rec.complete()
        report = m.write_report(rec)
        assert report.type == "maintenance"
        assert m.inspect_vehicle(truck)
        assert m.estimate_cost(2) == 80
        with pytest.raises(ValueError):
            Mechanic("n", 1, date.today(), "", "c")
        with pytest.raises(ValueError):
            Mechanic("n", 1, date.today(), "s", "")
        with pytest.raises(ValueError):
            m.inspect_vehicle(None)
        with pytest.raises(ValueError):
            m.repair(None)
        with pytest.raises(ValueError):
            m.write_report(None)
        with pytest.raises(ValueError):
            m.estimate_cost(0)
