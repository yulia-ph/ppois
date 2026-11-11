import pytest

from logistics_cargo.FragileCargo import FragileCargo


class TestFragileCargo:
    def test_fragile(self, address, address_warsaw):
        f = FragileCargo(5, 1, address, address_warsaw, "glass")
        f.require_label()
        assert f.check_orientation()
        assert f.estimate_packing() == 10
        with pytest.raises(ValueError):
            FragileCargo(1, 1, address, address_warsaw, "")
        with pytest.raises(ValueError):
            FragileCargo(1, 1, address, address_warsaw, "g", min_insurance=-1)
