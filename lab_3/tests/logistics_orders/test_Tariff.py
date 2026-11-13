import pytest

from logistics_orders.Tariff import Tariff


class TestTariff:
    def test_tariff(self, cargo, route):
        t = Tariff("std", 2, 1, 100)
        cargo.pack()
        price = t.calculate_price(cargo, route)
        assert price >= 100
        t.apply_surcharge(10)
        t.deactivate()
        with pytest.raises(ValueError):
            t.calculate_price(cargo, route)
        with pytest.raises(ValueError):
            Tariff("", 1, 1, 1)
        with pytest.raises(ValueError):
            Tariff("n", -1, 1, 1)
        t2 = Tariff("n", 1, 1, 1)
        with pytest.raises(ValueError):
            t2.is_applicable(None)
        with pytest.raises(ValueError):
            t2.apply_surcharge(-1)
        t2.deactivate()
        with pytest.raises(ValueError):
            t2.apply_surcharge(1)
        t3 = Tariff("n", 1, 1, 1)
        with pytest.raises(ValueError):
            t3.calculate_price(cargo, None)
