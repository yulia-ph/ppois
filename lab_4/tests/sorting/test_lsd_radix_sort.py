import pytest

from sorting.lsd_radix_sort import lsd_radix_sort
from sorting.Parcel import Parcel


def test_empty_and_single():
    assert lsd_radix_sort([]) == []
    assert lsd_radix_sort([4]) == [4]


def test_non_negative():
    data = [170, 45, 75, 90, 802, 24, 2, 66]
    lsd_radix_sort(data)
    assert data == [2, 24, 45, 66, 75, 90, 170, 802]


def test_negatives_and_zero():
    data = [3, -1, 0, -12, 8]
    lsd_radix_sort(data)
    assert data == [-12, -1, 0, 3, 8]


def test_duplicates():
    data = [5, 5, 1, 1, 5]
    lsd_radix_sort(data)
    assert data == [1, 1, 5, 5, 5]


def test_key_on_parcels(parcels):
    lsd_radix_sort(parcels, key=lambda parcel: parcel.weight)
    assert [p.weight for p in parcels] == [4, 9, 12]


def test_rejects_non_int():
    with pytest.raises(TypeError):
        lsd_radix_sort(["a", "b"])
    with pytest.raises(TypeError):
        lsd_radix_sort([Parcel("A", 1)])
