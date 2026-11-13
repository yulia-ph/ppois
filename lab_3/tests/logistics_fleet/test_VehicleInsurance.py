from datetime import date, timedelta

import pytest

from exceptions.InvalidCargoStateException import InvalidCargoStateException
from logistics_fleet.VehicleInsurance import VehicleInsurance


class TestVehicleInsurance:
    def test_insurance(self, truck):
        pol = VehicleInsurance(truck, "Ingo", 10_000, date.today() + timedelta(days=30))
        assert pol.is_active()
        pol.renew(10)
        pol.claim(100)
        with pytest.raises(InvalidCargoStateException):
            pol.claim(1)
        pol2 = VehicleInsurance(truck, "Ingo", 10_000, date.today() + timedelta(days=10))
        pol2.cancel()
        with pytest.raises(InvalidCargoStateException):
            pol2.renew(5)
        with pytest.raises(InvalidCargoStateException):
            pol2.cancel()
        with pytest.raises(ValueError):
            VehicleInsurance(None, "c", 1, date.today())
        with pytest.raises(ValueError):
            VehicleInsurance(truck, "", 1, date.today())
        with pytest.raises(ValueError):
            VehicleInsurance(truck, "c", 0, date.today())
        with pytest.raises(ValueError):
            VehicleInsurance(truck, "c", 1, None)
        pol3 = VehicleInsurance(truck, "c", 100, date.today() + timedelta(days=5))
        with pytest.raises(ValueError):
            pol3.renew(0)
        with pytest.raises(ValueError):
            pol3.claim(0)
        with pytest.raises(ValueError):
            pol3.claim(9999)
