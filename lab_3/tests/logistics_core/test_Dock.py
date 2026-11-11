import pytest

from exceptions.HazardousRestrictionException import HazardousRestrictionException
from logistics_core.Dock import Dock
from logistics_fleet.Tanker import Tanker


class TestDock:
    def test_occupy_release(self, truck):
        dock = Dock(1, 20.0)
        assert dock.is_free()
        assert dock.can_accept(truck)
        dock.occupy(truck)
        assert dock.is_occupied
        assert not dock.can_accept(truck)
        dock.release()
        assert dock.is_free()

    def test_dirty_tanker_rejected(self):
        dock = Dock(1, 20.0)
        tanker = Tanker("TT-1", "VIN-T", 8000, 20, 15.0, "3")
        tanker.load_liquid(1.0, "3")
        with pytest.raises(HazardousRestrictionException):
            dock.can_accept(tanker)

    def test_short_dock_tanker(self):
        dock = Dock(1, 8.0)
        tanker = Tanker("TT-2", "VIN-T2", 8000, 20, 15.0, "3")
        with pytest.raises(HazardousRestrictionException):
            dock.can_accept(tanker)

    def test_dock_validation(self):
        with pytest.raises(ValueError):
            Dock(0, 10)
        with pytest.raises(ValueError):
            Dock(1, 0)
        dock = Dock(1, 10)
        with pytest.raises(ValueError):
            dock.can_accept(None)
        with pytest.raises(ValueError):
            dock.occupy(None)
