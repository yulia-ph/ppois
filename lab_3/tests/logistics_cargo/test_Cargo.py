import pytest

from exceptions.CargoOverweightException import CargoOverweightException
from exceptions.InvalidCargoStateException import InvalidCargoStateException
from logistics_cargo.Cargo import Cargo


class TestCargo:
    def test_pack_unpack(self, cargo):
        cargo.pack()
        cargo.unpack()
        cargo.pack()
        cargo.update_status(Cargo.STATUS_IN_TRANSIT)
        cargo.mark_damaged()
        with pytest.raises(InvalidCargoStateException):
            cargo.mark_damaged()
        with pytest.raises(InvalidCargoStateException):
            cargo.update_status(Cargo.STATUS_PACKED)

    def test_can_fit(self, cargo):
        assert cargo.can_fit(200)
        with pytest.raises(CargoOverweightException):
            cargo.can_fit(10)

    def test_validation(self, address, address_warsaw):
        with pytest.raises(ValueError):
            Cargo(0, 1, address, address_warsaw)
        with pytest.raises(ValueError):
            Cargo(1, 0, address, address_warsaw)
        with pytest.raises(ValueError):
            Cargo(1, 1, None, address_warsaw)
        with pytest.raises(ValueError):
            Cargo(1, 1, address, address_warsaw, declared_value=-1)
        c = Cargo(1, 1, address, address_warsaw)
        with pytest.raises(ValueError):
            c.can_fit(0)
        with pytest.raises(ValueError):
            c.update_status("nope")
        with pytest.raises(InvalidCargoStateException):
            c.unpack()
        c.pack()
        with pytest.raises(InvalidCargoStateException):
            c.pack()
