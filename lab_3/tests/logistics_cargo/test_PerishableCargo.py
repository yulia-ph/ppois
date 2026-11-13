from datetime import date, timedelta

import pytest

from logistics_cargo.PerishableCargo import PerishableCargo


class TestPerishableCargo:
    def test_perishable(self, address, address_warsaw):
        p = PerishableCargo(5, 1, address, address_warsaw, 0, 8, date.today())
        assert p.check_temperature(4)
        assert not p.is_expired()
        p.extend_shelf_life(3)
        with pytest.raises(ValueError):
            PerishableCargo(1, 1, address, address_warsaw, 8, 0, date.today())
        with pytest.raises(ValueError):
            PerishableCargo(1, 1, address, address_warsaw, 0, 8, None)
        with pytest.raises(ValueError):
            p.extend_shelf_life(0)
        old = PerishableCargo(1, 1, address, address_warsaw, 0, 8, date.today() - timedelta(days=2))
        assert old.is_expired()
