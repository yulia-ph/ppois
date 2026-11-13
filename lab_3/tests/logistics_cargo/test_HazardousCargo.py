import pytest

from exceptions.HazardousRestrictionException import HazardousRestrictionException
from logistics_cargo.Cargo import Cargo
from logistics_cargo.HazardousCargo import HazardousCargo


class TestHazardousCargo:
    def test_hazardous(self, address, address_warsaw):
        a = HazardousCargo(10, 1, address, address_warsaw, "UN1", "1")
        b = HazardousCargo(10, 1, address, address_warsaw, "UN3", "3")
        c = Cargo(1, 1, address, address_warsaw)
        assert a.compatible_with(c)
        with pytest.raises(HazardousRestrictionException):
            a.compatible_with(b)
        assert a.needs_permit()
        a.require_escort()
        with pytest.raises(ValueError):
            HazardousCargo(1, 1, address, address_warsaw, "", "1")
        with pytest.raises(ValueError):
            HazardousCargo(1, 1, address, address_warsaw, "u", "")
        with pytest.raises(ValueError):
            a.compatible_with(None)
