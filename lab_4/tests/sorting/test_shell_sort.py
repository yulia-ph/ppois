from sorting.Parcel import Parcel
from sorting.shell_sort import shell_sort


def test_empty_and_single():
    empty = []
    assert shell_sort(empty) == []
    one = [7]
    assert shell_sort(one) == [7]


def test_numbers_and_reverse():
    data = [5, 1, 4, 2, 8, 0]
    shell_sort(data)
    assert data == [0, 1, 2, 4, 5, 8]
    shell_sort(data, reverse=True)
    assert data == [8, 5, 4, 2, 1, 0]


def test_strings():
    words = ["pear", "apple", "fig"]
    shell_sort(words)
    assert words == ["apple", "fig", "pear"]


def test_parcels_by_natural_order(parcels):
    shell_sort(parcels)
    assert [p.weight for p in parcels] == [4, 9, 12]
    assert parcels[0].destination == "Minsk"


def test_key_function():
    words = ["bbb", "a", "cccc"]
    shell_sort(words, key=len)
    assert words == ["a", "bbb", "cccc"]
    items = [Parcel("Z", 3), Parcel("A", 3)]
    shell_sort(items)
    assert items[0].destination == "A"
