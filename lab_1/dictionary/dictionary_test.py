"""Tests for the Dictionary class."""
import json
import pytest
from dictionary import Dictionary


@pytest.fixture
def empty_dict():
    return Dictionary()


@pytest.fixture
def filled_dict():
    d = Dictionary()
    d.add_node("cat", "кот")
    d.add_node("dog", "пёс")
    d.add_node("sun", "солнце")
    return d


def test_add_to_empty(empty_dict):
    assert empty_dict.add_node("cat", "кот") is True
    assert empty_dict.find_node("cat") == "кот"
    assert len(empty_dict) == 1


def test_add_new_returns_true(filled_dict):
    assert filled_dict.add_node("moon", "луна") is True
    assert len(filled_dict) == 4


def test_add_existing_returns_false(filled_dict):
    assert filled_dict.add_node("cat", "кошка") is False
    assert len(filled_dict) == 3


def test_add_existing_updates_value(filled_dict):
    filled_dict.add_node("cat", "кошка")
    assert filled_dict.find_node("cat") == "кошка"


def test_add_many_and_find_all(empty_dict):
    words = [("dog", "пёс"), ("cat", "кот"), ("sun", "солнце"),
             ("moon", "луна"), ("star", "звезда")]
    for k, v in words:
        empty_dict.add_node(k, v)
    for k, v in words:
        assert empty_dict.find_node(k) == v
    assert len(empty_dict) == 5


def test_find_existing(filled_dict):
    assert filled_dict.find_node("dog") == "пёс"


def test_find_missing_raises(filled_dict):
    with pytest.raises(KeyError):
        filled_dict.find_node("fish")


def test_find_in_empty_raises(empty_dict):
    with pytest.raises(KeyError):
        empty_dict.find_node("cat")


def test_find_missing_message_contains_key(filled_dict):
    with pytest.raises(KeyError, match="fish"):
        filled_dict.find_node("fish")


def test_delete_from_empty_returns_false(empty_dict):
    assert empty_dict.delete_node("cat") is False


def test_delete_missing_returns_false(filled_dict):
    assert filled_dict.delete_node("fish") is False
    assert len(filled_dict) == 3


def test_delete_leaf(empty_dict):
    empty_dict.add_node("cat", "кот")
    empty_dict.add_node("dog", "пёс")
    assert empty_dict.delete_node("dog") is True
    assert len(empty_dict) == 1
    with pytest.raises(KeyError):
        empty_dict.find_node("dog")


def test_delete_node_with_left_child_only(empty_dict):
    empty_dict.add_node("dog", "пёс")
    empty_dict.add_node("cat", "кот")
    assert empty_dict.delete_node("dog") is True
    assert empty_dict.find_node("cat") == "кот"
    assert len(empty_dict) == 1


def test_delete_node_with_right_child_only(empty_dict):
    empty_dict.add_node("cat", "кот")
    empty_dict.add_node("dog", "пёс")
    assert empty_dict.delete_node("cat") is True
    assert empty_dict.find_node("dog") == "пёс"
    assert len(empty_dict) == 1


def test_delete_node_with_two_children(empty_dict):
    for k, v in [("dog", "пёс"), ("cat", "кот"), ("sun", "солнце"),
                 ("moon", "луна"), ("star", "звезда")]:
        empty_dict.add_node(k, v)
    assert empty_dict.delete_node("dog") is True
    assert len(empty_dict) == 4
    with pytest.raises(KeyError):
        empty_dict.find_node("dog")
    for k, v in [("cat", "кот"), ("sun", "солнце"),
                 ("moon", "луна"), ("star", "звезда")]:
        assert empty_dict.find_node(k) == v


def test_delete_root_leaf(empty_dict):
    empty_dict.add_node("cat", "кот")
    assert empty_dict.delete_node("cat") is True
    assert len(empty_dict) == 0


def test_delete_root_with_one_child(empty_dict):
    empty_dict.add_node("cat", "кот")
    empty_dict.add_node("dog", "пёс")
    assert empty_dict.delete_node("cat") is True
    assert empty_dict.find_node("dog") == "пёс"
    assert len(empty_dict) == 1


def test_delete_root_with_two_children(empty_dict):
    for k, v in [("dog", "пёс"), ("cat", "кот"), ("sun", "солнце")]:
        empty_dict.add_node(k, v)
    assert empty_dict.delete_node("dog") is True
    assert empty_dict.find_node("cat") == "кот"
    assert empty_dict.find_node("sun") == "солнце"
    assert len(empty_dict) == 2


def test_delete_all_then_empty(empty_dict):
    for k in ["dog", "cat", "sun", "moon", "star"]:
        empty_dict.add_node(k, k)
    for k in ["moon", "dog", "star", "cat", "sun"]:
        assert empty_dict.delete_node(k) is True
    assert len(empty_dict) == 0
    assert empty_dict.pack_dictionary() == {}


def test_len_empty(empty_dict):
    assert len(empty_dict) == 0


def test_len_after_adds(filled_dict):
    assert len(filled_dict) == 3


def test_len_not_changed_on_update(filled_dict):
    filled_dict.add_node("cat", "кошка")
    assert len(filled_dict) == 3


def test_len_after_delete(filled_dict):
    filled_dict.delete_node("dog")
    assert len(filled_dict) == 2


def test_pack_empty(empty_dict):
    assert empty_dict.pack_dictionary() == {}


def test_pack_returns_all_pairs(filled_dict):
    result = filled_dict.pack_dictionary()
    assert result == {"cat": "кот", "dog": "пёс", "sun": "солнце"}


def test_pack_is_sorted_by_key(empty_dict):
    for k in ["moon", "cat", "sun", "dog", "star"]:
        empty_dict.add_node(k, k)
    keys = list(empty_dict.pack_dictionary().keys())
    assert keys == sorted(keys)


def test_save_and_load_roundtrip(filled_dict, tmp_path):
    file = tmp_path / "d.json"
    filled_dict.save_dictionary(file)

    new_dict = Dictionary()
    new_dict.load_dictionary(file)

    assert new_dict.pack_dictionary() == filled_dict.pack_dictionary()
    assert len(new_dict) == len(filled_dict)


def test_save_creates_valid_json(filled_dict, tmp_path):
    file = tmp_path / "d.json"
    filled_dict.save_dictionary(file)

    with file.open(encoding="utf-8") as f:
        data = json.load(f)
    assert data == {"cat": "кот", "dog": "пёс", "sun": "солнце"}


def test_save_preserves_cyrillic(filled_dict, tmp_path):
    file = tmp_path / "d.json"
    filled_dict.save_dictionary(file)
    text = file.read_text(encoding="utf-8")
    assert "кот" in text


def test_load_missing_file(tmp_path):
    d = Dictionary()
    with pytest.raises(FileNotFoundError):
        d.load_dictionary(tmp_path / "nope.json")


def test_load_bad_json(tmp_path):
    file = tmp_path / "bad.json"
    file.write_text("{not json", encoding="utf-8")
    d = Dictionary()
    with pytest.raises(json.JSONDecodeError):
        d.load_dictionary(file)


def test_load_non_object(tmp_path):
    file = tmp_path / "list.json"
    file.write_text("[1, 2, 3]", encoding="utf-8")
    d = Dictionary()
    with pytest.raises(TypeError):
        d.load_dictionary(file)


def test_load_non_string_key(tmp_path):
    file = tmp_path / "val.json"
    file.write_text('{"cat": 42}', encoding="utf-8")
    d = Dictionary()
    with pytest.raises(TypeError):
        d.load_dictionary(file)


def test_load_replaces_existing(filled_dict, tmp_path):
    file = tmp_path / "new.json"
    file.write_text('{"moon": "луна"}', encoding="utf-8")
    filled_dict.load_dictionary(file)
    assert filled_dict.pack_dictionary() == {"moon": "луна"}
    assert len(filled_dict) == 1


def test_load_atomic_on_bad_data(empty_dict, tmp_path):
    empty_dict.add_node("cat", "кот")
    bad = tmp_path / "bad.json"
    bad.write_text('{"dog": "пёс", "sun": 42}', encoding="utf-8")
    with pytest.raises(TypeError):
        empty_dict.load_dictionary(bad)
    assert empty_dict.pack_dictionary() == {"cat": "кот"}
    assert len(empty_dict) == 1