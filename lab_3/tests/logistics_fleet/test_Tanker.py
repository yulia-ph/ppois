import pytest

from exceptions.InvalidCargoStateException import InvalidCargoStateException
from logistics_fleet.Tanker import Tanker


class TestTanker:
    def test_tanker(self):
        tanker = Tanker("TK-1", "VIN-K", 8000, 20, 12.0, "3")
        assert tanker.is_compatible("5")
        tanker.load_liquid(2.0, "3")
        assert not tanker.is_cleaned
        tanker.unload_liquid()
        tanker.clean_tank()
        assert tanker.is_cleaned
        with pytest.raises(ValueError):
            Tanker("a", "b", 1, 1, 0, "3")
        with pytest.raises(ValueError):
            Tanker("a", "b", 1, 1, 1, "")
        with pytest.raises(ValueError):
            tanker.is_compatible("")
        with pytest.raises(ValueError):
            tanker.load_liquid(0, "3")
        tanker.load_liquid(1, "3")
        from exceptions.HazardousRestrictionException import HazardousRestrictionException
        with pytest.raises(HazardousRestrictionException):
            tanker.load_liquid(1, "1")
        tanker.unload_liquid()
        tanker.load_liquid(12, "3")
        with pytest.raises(InvalidCargoStateException):
            tanker.load_liquid(1, "3")
        tanker.unload_liquid()
        tanker.load_liquid(1, "3")
        with pytest.raises(InvalidCargoStateException):
            tanker.clean_tank()
        tanker.unload_liquid()
        with pytest.raises(InvalidCargoStateException):
            tanker.unload_liquid()
