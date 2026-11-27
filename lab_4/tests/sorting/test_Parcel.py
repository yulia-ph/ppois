import pytest

from sorting.Parcel import Parcel


def test_properties_and_compare():
    light = Parcel("Minsk", 2)
    heavy = Parcel("Warsaw", 10)
    also_light = Parcel("Grodno", 2)
    assert light.destination == "Minsk"
    assert light.weight == 2
    assert light < heavy
    assert also_light < light
    assert light == Parcel("Minsk", 2)
    assert light != heavy
    assert "Minsk" in repr(light)
    assert light.__eq__("x") is NotImplemented
    assert light.__lt__("x") is NotImplemented


def test_validation():
    with pytest.raises(ValueError):
        Parcel("", 1)
    with pytest.raises(ValueError):
        Parcel("Minsk", 0)
