import pytest

from exceptions.VehicleNotAvailableException import VehicleNotAvailableException
from exceptions.VehicleOverloadException import VehicleOverloadException
from logistics_fleet.Vehicle import Vehicle


class TestVehicle:
    def test_trip_and_load(self, truck, cargo, gps):
        truck.locate(gps)
        assert truck.gps is gps
        assert truck.can_load(cargo)
        truck.start_trip()
        truck.finish_trip(10)
        truck.refuel(5)
        with pytest.raises(VehicleOverloadException):
            heavy = type("C", (), {"weight": 99_999, "volume": 1})()
            truck.can_load(heavy)

    def test_not_available(self, truck):
        truck.start_trip()
        with pytest.raises(VehicleNotAvailableException):
            truck.start_trip()
        truck._fuel_level = 0
        truck._status = Vehicle.STATUS_IDLE
        with pytest.raises(VehicleNotAvailableException):
            truck.start_trip()

    def test_validation(self):
        with pytest.raises(ValueError):
            Vehicle("", "v", 1, 1)
        with pytest.raises(ValueError):
            Vehicle("p", "", 1, 1)
        with pytest.raises(ValueError):
            Vehicle("p", "v", 0, 1)
        with pytest.raises(ValueError):
            Vehicle("p", "v", 1, 0)
        v = Vehicle("p", "v", 1, 1)
        with pytest.raises(ValueError):
            v.assign_driver(None)
        with pytest.raises(VehicleNotAvailableException):
            v.finish_trip(1)
        v.start_trip()
        with pytest.raises(ValueError):
            v.finish_trip(-1)
        with pytest.raises(ValueError):
            v.refuel(0)
        with pytest.raises(ValueError):
            v.can_load(None)
        with pytest.raises(ValueError):
            v.locate(None)
        with pytest.raises(VehicleOverloadException):
            v.can_load(type("C", (), {"weight": 0.5, "volume": 99})())
