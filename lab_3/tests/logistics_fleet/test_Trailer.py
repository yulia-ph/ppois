import pytest

from exceptions.InvalidCargoStateException import InvalidCargoStateException
from logistics_fleet.Trailer import Trailer
from logistics_fleet.Truck import Truck


class TestTrailer:
    def test_trailer_errors(self):
        with pytest.raises(ValueError):
            Trailer("", 1, Trailer.TYPE_FLATBED)
        with pytest.raises(ValueError):
            Trailer("p", 0, Trailer.TYPE_FLATBED)
        with pytest.raises(ValueError):
            Trailer("p", 1, "nope")
        t = Trailer("p", 10, Trailer.TYPE_REEFER)
        with pytest.raises(InvalidCargoStateException):
            t.detach()
        with pytest.raises(ValueError):
            t.attach(None)
        t.attach(object())
        with pytest.raises(InvalidCargoStateException):
            t.attach(object())
        assert t.remaining_capacity() == 10
        truck = Truck("A", "V", 100, 10, 2)
        with pytest.raises(ValueError):
            truck.can_take_trailer(None)
        with pytest.raises(ValueError):
            truck.unhitch()
        with pytest.raises(ValueError):
            Truck("A", "V", 100, 10, 1)
