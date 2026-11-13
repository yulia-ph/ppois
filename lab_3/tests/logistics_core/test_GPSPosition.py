import pytest

from logistics_core.GPSPosition import GPSPosition


class TestGPSPosition:
    def test_init_and_distance(self):
        a = GPSPosition(53.9, 27.56)
        b = GPSPosition(52.23, 21.01)
        assert a.distance_to(b) > 100
        assert a.is_valid()

    def test_invalid_lat(self):
        with pytest.raises(ValueError):
            GPSPosition(100, 0)

    def test_invalid_lon(self):
        with pytest.raises(ValueError):
            GPSPosition(0, 200)

    def test_negative_accuracy(self):
        with pytest.raises(ValueError):
            GPSPosition(0, 0, accuracy=-1)

    def test_update_and_move(self):
        a = GPSPosition(0, 0)
        a.update(1, 1, accuracy=5)
        assert a.latitude == 1
        other = GPSPosition(2, 2)
        a.move_towards(other, 0.5)
        assert a.latitude == pytest.approx(1.5)

    def test_update_bad(self):
        a = GPSPosition(0, 0)
        with pytest.raises(ValueError):
            a.update(99, 0)
        with pytest.raises(ValueError):
            a.update(0, 200)
        with pytest.raises(ValueError):
            a.update(0, 0, accuracy=-1)
        with pytest.raises(ValueError):
            a.distance_to(None)
        with pytest.raises(ValueError):
            a.move_towards(None, 0.5)
        with pytest.raises(ValueError):
            a.move_towards(GPSPosition(1, 1), 2)
