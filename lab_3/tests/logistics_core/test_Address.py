import pytest

from logistics_core.Address import Address


class TestAddress:
    def test_format_and_city(self, address, address_warsaw):
        assert address.is_same_city(address)
        assert not address.is_same_city(address_warsaw)
        assert address.in_country("Belarus")
        assert address.is_complete()
        assert "Minsk" in address.format()
        assert address.distance_to(address_warsaw) > 0

    def test_empty_city(self):
        with pytest.raises(ValueError):
            Address("s", "", "r", "c", "1")

    def test_empty_country(self):
        with pytest.raises(ValueError):
            Address("s", "city", "r", "", "1")

    def test_incomplete_and_none_coords(self):
        a = Address("", "Minsk", "", "Belarus", "")
        assert not a.is_complete()
        b = Address("x", "Minsk", "", "Belarus", "1")
        assert a.distance_to(b) == 0
        with pytest.raises(ValueError):
            a.is_same_city(None)
        with pytest.raises(ValueError):
            a.in_country("")
        with pytest.raises(ValueError):
            a.distance_to(None)
