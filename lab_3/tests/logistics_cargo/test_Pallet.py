import pytest

from exceptions.CargoOverweightException import CargoOverweightException
from exceptions.InvalidCargoStateException import InvalidCargoStateException
from logistics_cargo.Package import Package
from logistics_cargo.Pallet import Pallet


class TestPallet:
    def test_pallet_errors(self, cargo):
        with pytest.raises(ValueError):
            Pallet("", 1)
        with pytest.raises(ValueError):
            Pallet("p", 0)
        pal = Pallet("p", 500)
        with pytest.raises(ValueError):
            pal.add_package(None)
        pal.wrap()
        with pytest.raises(InvalidCargoStateException):
            pal.add_package(Package(cargo, 1))
        with pytest.raises(InvalidCargoStateException):
            pal.wrap()
        pal.unwrap()
        with pytest.raises(InvalidCargoStateException):
            pal.unwrap()
        pal.add_package(Package(cargo, 1))
        with pytest.raises(ValueError):
            pal.add_package(pal.packages[0])
        heavy = Pallet("h", 1)
        from logistics_cargo.Cargo import Cargo as C
        from logistics_core.Address import Address
        from logistics_core.GPSPosition import GPSPosition
        a = Address("s", "c", "r", "co", "1", GPSPosition(0, 0))
        big = C(10, 1, a, a)
        with pytest.raises(CargoOverweightException):
            heavy.add_package(Package(big, 1))
