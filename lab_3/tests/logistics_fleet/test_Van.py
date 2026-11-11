import pytest

from exceptions.InvalidCargoStateException import InvalidCargoStateException
from logistics_fleet.Van import Van


class TestVan:
    def test_van_liftgate(self, truck):
        van = Van("VN-1", "VIN-V", 1200, 8, door_count=2, has_liftgate=True)
        van.open_doors()
        van.use_liftgate()
        van.close_doors()
        with pytest.raises(InvalidCargoStateException):
            van.use_liftgate()
        van2 = Van("VN-2", "VIN-V2", 1200, 8, 2, has_liftgate=False)
        van2.open_doors()
        with pytest.raises(InvalidCargoStateException):
            van2.use_liftgate()
        with pytest.raises(ValueError):
            Van("x", "y", 1, 1, 0)
