import pytest

from exceptions.InvalidCargoStateException import InvalidCargoStateException
from exceptions.VehicleOverloadException import VehicleOverloadException
from logistics_cargo.Container import Container
from logistics_cargo.Package import Package
from logistics_cargo.Pallet import Pallet


class TestContainer:
    def test_container_errors(self, cargo):
        with pytest.raises(ValueError):
            Container("", 1)
        with pytest.raises(ValueError):
            Container("i", 0)
        c = Container("i", 1000)
        with pytest.raises(ValueError):
            c.load_pallet(None)
        pal = Pallet("p", 500)
        pal.add_package(Package(cargo, 1))
        c.load_pallet(pal)
        c.seal("s")
        with pytest.raises(InvalidCargoStateException):
            c.load_pallet(pal)
        with pytest.raises(InvalidCargoStateException):
            c.unload_pallet(pal)
        with pytest.raises(InvalidCargoStateException):
            c.seal("x")
        c2 = Container("i2", 10)
        with pytest.raises(ValueError):
            c2.seal("")
        with pytest.raises(ValueError):
            c2.unload_pallet(pal)
        assert not c2.inspect()
        tiny = Container("t", 1)
        pal2 = Pallet("p2", 500)
        pal2.add_package(Package(cargo, 1))
        with pytest.raises(VehicleOverloadException):
            tiny.load_pallet(pal2)
