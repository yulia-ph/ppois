import pytest

from exceptions.HazardousRestrictionException import HazardousRestrictionException
from logistics_cargo.HazardousCargo import HazardousCargo
from logistics_core.Checkpoint import Checkpoint


class TestCheckpoint:
    def test_inspect_ok(self, address, cargo):
        cp = Checkpoint("Border", address, is_border=True)
        cp.require_document("passport")
        assert cp.inspect(cargo)

    def test_hazardous_needs_permit(self, address, address_warsaw):
        cp = Checkpoint("Border", address, True)
        hz = HazardousCargo(10, 1, address, address_warsaw, "UN1203", "1")
        with pytest.raises(HazardousRestrictionException):
            cp.inspect(hz)

    def test_deny(self, address, cargo):
        cp = Checkpoint("CP", address)
        with pytest.raises(HazardousRestrictionException):
            cp.deny_passage("no papers")
        cp._is_open = False
        with pytest.raises(ValueError):
            cp.inspect(cargo)
        with pytest.raises(ValueError):
            Checkpoint("", address)
        with pytest.raises(ValueError):
            Checkpoint("CP", None)
        with pytest.raises(ValueError):
            cp.require_document("")
        cp2 = Checkpoint("CP2", address)
        cp2.require_document("cmr")
        with pytest.raises(ValueError):
            cp2.require_document("cmr")
        with pytest.raises(ValueError):
            cp2.inspect(None)
        with pytest.raises(ValueError):
            cp2.deny_passage("")
