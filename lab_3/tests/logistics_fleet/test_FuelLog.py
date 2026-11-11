import pytest

from logistics_fleet.FuelLog import FuelLog


class TestFuelLog:
    def test_fuel_log(self, truck):
        log = FuelLog(truck, 40, 80, "Belorusneft", 1100)
        log.record()
        assert log.consumption_per_100km(1000) == pytest.approx(40)
        assert not log.is_anomaly(1000)
        with pytest.raises(ValueError):
            log.consumption_per_100km(1100)
        with pytest.raises(ValueError):
            FuelLog(None, 1, 1, "s", 1)
        with pytest.raises(ValueError):
            FuelLog(truck, 0, 1, "s", 1)
        with pytest.raises(ValueError):
            FuelLog(truck, 1, -1, "s", 1)
        with pytest.raises(ValueError):
            FuelLog(truck, 1, 1, "", 1)
        with pytest.raises(ValueError):
            FuelLog(truck, 1, 1, "s", -1)
        big = FuelLog(truck, 90, 1, "s", 1100)
        assert big.is_anomaly(1000)
