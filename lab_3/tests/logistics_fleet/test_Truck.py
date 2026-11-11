import pytest

from exceptions.VehicleOverloadException import VehicleOverloadException
from logistics_fleet.Trailer import Trailer


class TestTruck:
    def test_hitch(self, truck):
        trailer = Trailer("TR-1", 5000, Trailer.TYPE_FLATBED)
        truck.hitch_trailer(trailer)
        assert trailer.is_attached
        assert truck.axle_load() > 0
        truck.unhitch()
        assert not trailer.is_attached

    def test_overload_trailer(self, truck):
        huge = Trailer("TR-2", 50_000, Trailer.TYPE_CURTAIN)
        with pytest.raises(VehicleOverloadException):
            truck.hitch_trailer(huge)
