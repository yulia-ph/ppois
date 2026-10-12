"""Tests for the museum_exhibits package.

Covers: Exhibit, Painting, Sculpture, Document, Collection, Fund,
Catalog, DigitalCopy. Sections are added as each class is implemented.
"""

import pytest

from exceptions.ExhibitNotFoundException import ExhibitNotFoundException
from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
from tests.conftest import FakeExhibitForCatalog, FakeExhibitForCollection


class TestCatalogInit:
    def test_init_empty(self, catalog):
        assert catalog.items == []
        assert catalog.count() == 0
        assert catalog.is_empty is True


class TestCatalogAdd:
    def test_add_success(self, catalog):
        ex = FakeExhibitForCatalog("EX-001")
        assert catalog.add(ex) is True
        assert ex in catalog.items
        assert catalog.count() == 1
        assert catalog.is_empty is False

    def test_add_none_raises(self, catalog):
        with pytest.raises(ValueError):
            catalog.add(None)

    def test_add_duplicate_object_raises(self, catalog):
        ex = FakeExhibitForCatalog("EX-001")
        catalog.add(ex)
        with pytest.raises(ValueError):
            catalog.add(ex)

    def test_add_duplicate_inventory_number_raises(self, catalog):
        catalog.add(FakeExhibitForCatalog("EX-001"))
        other = FakeExhibitForCatalog("EX-001")
        with pytest.raises(ValueError):
            catalog.add(other)


class TestCatalogRemove:
    def test_remove_success(self, catalog):
        ex = FakeExhibitForCatalog("EX-001")
        catalog.add(ex)
        assert catalog.remove(ex) is True
        assert catalog.is_empty is True

    def test_remove_none_raises(self, catalog):
        with pytest.raises(ValueError):
            catalog.remove(None)

    def test_remove_not_present_raises(self, catalog):
        with pytest.raises(ValueError):
            catalog.remove(FakeExhibitForCatalog("EX-001"))

    def test_remove_twice_raises(self, catalog):
        ex = FakeExhibitForCatalog("EX-001")
        catalog.add(ex)
        catalog.remove(ex)
        with pytest.raises(ValueError):
            catalog.remove(ex)

    def test_remove_then_add_same_number_allowed(self, catalog):
        """After removal, the inventory number is free again."""
        ex1 = FakeExhibitForCatalog("EX-001")
        catalog.add(ex1)
        catalog.remove(ex1)
        ex2 = FakeExhibitForCatalog("EX-001")
        assert catalog.add(ex2) is True


class TestCatalogFindByNumber:
    def test_find_success(self, catalog_with_exhibits):
        found = catalog_with_exhibits.find_by_number("EX-002")
        assert found.title == "Sunflowers"

    def test_find_not_found_raises(self, catalog_with_exhibits):
        from exceptions.ExhibitNotFoundException import ExhibitNotFoundException
        with pytest.raises(ExhibitNotFoundException):
            catalog_with_exhibits.find_by_number("EX-999")

    def test_find_in_empty_catalog_raises(self, catalog):
        from exceptions.ExhibitNotFoundException import ExhibitNotFoundException
        with pytest.raises(ExhibitNotFoundException):
            catalog.find_by_number("EX-001")


class TestCatalogSearch:
    def test_search_by_title(self, catalog_with_exhibits):
        result = catalog_with_exhibits.search("mona")
        assert len(result) == 1
        assert result[0].inventory_number == "EX-001"

    def test_search_by_author(self, catalog_with_exhibits):
        result = catalog_with_exhibits.search("van gogh")
        assert len(result) == 2

    def test_search_case_insensitive(self, catalog_with_exhibits):
        assert len(catalog_with_exhibits.search("MONA")) == 1
        assert len(catalog_with_exhibits.search("Mona")) == 1
        assert len(catalog_with_exhibits.search("mona")) == 1

    def test_search_partial_match(self, catalog_with_exhibits):
        result = catalog_with_exhibits.search("star")
        assert len(result) == 1
        assert result[0].inventory_number == "EX-003"

    def test_search_no_results(self, catalog_with_exhibits):
        assert catalog_with_exhibits.search("Picasso") == []

    def test_search_empty_string_raises(self, catalog_with_exhibits):
        with pytest.raises(ValueError):
            catalog_with_exhibits.search("")

    def test_search_none_raises(self, catalog_with_exhibits):
        with pytest.raises(ValueError):
            catalog_with_exhibits.search(None)


class TestCatalogFilterByCondition:
    def test_filter_excellent(self, catalog_with_exhibits):
        result = catalog_with_exhibits.filter_by_condition("excellent")
        assert len(result) == 1
        assert result[0].inventory_number == "EX-001"

    def test_filter_good(self, catalog_with_exhibits):
        result = catalog_with_exhibits.filter_by_condition("good")
        assert len(result) == 1

    def test_filter_no_match(self, catalog_with_exhibits):
        assert catalog_with_exhibits.filter_by_condition("critical") == []


class TestCatalogFilterByCollection:
    def test_filter_matching_collection(self, catalog_with_exhibits, sample_exhibits):
        collection_a = object()
        sample_exhibits[0].collection = collection_a
        sample_exhibits[1].collection = collection_a
        result = catalog_with_exhibits.filter_by_collection(collection_a)
        assert len(result) == 2

    def test_filter_no_match(self, catalog_with_exhibits):
        result = catalog_with_exhibits.filter_by_collection(object())
        assert result == []


class TestCatalogFilterByAuthor:
    def test_filter_single(self, catalog_with_exhibits):
        result = catalog_with_exhibits.filter_by_author("Leonardo")
        assert len(result) == 1

    def test_filter_multiple(self, catalog_with_exhibits):
        result = catalog_with_exhibits.filter_by_author("Van Gogh")
        assert len(result) == 2

    def test_filter_no_match(self, catalog_with_exhibits):
        assert catalog_with_exhibits.filter_by_author("Picasso") == []


class TestCatalogFilterByClass:
    def test_filter_fake_class(self, catalog_with_exhibits):
        result = catalog_with_exhibits.filter_by_class("FakeExhibitForCatalog")
        assert len(result) == 3

    def test_filter_unknown_class(self, catalog_with_exhibits):
        assert catalog_with_exhibits.filter_by_class("Painting") == []


class TestCatalogCount:
    def test_count_empty(self, catalog):
        assert catalog.count() == 0

    def test_count_with_items(self, catalog_with_exhibits):
        assert catalog_with_exhibits.count() == 3


class TestCatalogTotalValue:
    def test_total_value_empty(self, catalog):
        assert catalog.total_value() == 0

    def test_total_value_with_items(self, catalog_with_exhibits):
        # 1000 + 500 + 800 = 2300
        assert catalog_with_exhibits.total_value() == 2300.0


class TestCatalogByConditionStats:
    def test_stats_empty(self, catalog):
        assert catalog.by_condition_stats() == {}

    def test_stats_with_items(self, catalog_with_exhibits):
        stats = catalog_with_exhibits.by_condition_stats()
        assert stats["excellent"] == 1
        assert stats["good"] == 1
        assert stats["damaged"] == 1

    def test_stats_aggregates_same_condition(self, catalog):
        catalog.add(FakeExhibitForCatalog("EX-001", condition="good"))
        catalog.add(FakeExhibitForCatalog("EX-002", condition="good"))
        catalog.add(FakeExhibitForCatalog("EX-003", condition="damaged"))
        stats = catalog.by_condition_stats()
        assert stats["good"] == 2
        assert stats["damaged"] == 1


class TestCollectionInit:
    def test_init_stores_fields(self, collection):
        assert collection.name == "Dutch Golden Age"
        assert collection.theme == "17th-century Dutch painting"

    def test_init_no_curator(self, collection):
        assert collection.curator is None

    def test_init_exhibits_empty(self, collection):
        assert collection.exhibits == []
        assert collection.is_empty is True

    def test_init_empty_name_raises(self):
        from museum_exhibits.Collection import Collection
        with pytest.raises(ValueError):
            Collection("", "theme")

    def test_init_empty_theme_raises(self):
        from museum_exhibits.Collection import Collection
        with pytest.raises(ValueError):
            Collection("name", "")


class TestCollectionCurator:
    def test_set_curator_success(self, collection):
        curator = object()
        assert collection.set_curator(curator) is True
        assert collection.curator is curator

    def test_set_curator_none_raises(self, collection):
        with pytest.raises(ValueError):
            collection.set_curator(None)

    def test_remove_curator_success(self, collection):
        collection.set_curator(object())
        assert collection.remove_curator() is True
        assert collection.curator is None

    def test_remove_curator_idempotent(self, collection):
        """Removing when no curator is set is not an error."""
        assert collection.remove_curator() is True
        assert collection.curator is None


class TestCollectionAddExhibit:
    def test_add_success(self, collection):
        ex = FakeExhibitForCollection("EX-001")
        assert collection.add_exhibit(ex) is True
        assert ex in collection.exhibits
        assert collection.is_empty is False

    def test_add_none_raises(self, collection):
        with pytest.raises(ValueError):
            collection.add_exhibit(None)

    def test_add_duplicate_raises(self, collection):
        ex = FakeExhibitForCollection("EX-001")
        collection.add_exhibit(ex)
        with pytest.raises(ValueError):
            collection.add_exhibit(ex)

    def test_add_exhibit_in_other_collection_raises(self, collection):
        from museum_exhibits.Collection import Collection
        other = Collection("Other", "theme")
        ex = FakeExhibitForCollection("EX-001")
        other.add_exhibit(ex)
        with pytest.raises(InvalidExhibitStateException):
            collection.add_exhibit(ex)

    def test_add_attaches_exhibit_back(self, collection):
        """The exhibit remembers which collection it belongs to."""
        ex = FakeExhibitForCollection("EX-001")
        collection.add_exhibit(ex)
        assert ex._collection is collection


class TestCollectionRemoveExhibit:
    def test_remove_success(self, collection):
        ex = FakeExhibitForCollection("EX-001")
        collection.add_exhibit(ex)
        assert collection.remove_exhibit(ex) is True
        assert ex not in collection.exhibits

    def test_remove_detaches_exhibit(self, collection):
        ex = FakeExhibitForCollection("EX-001")
        collection.add_exhibit(ex)
        collection.remove_exhibit(ex)
        assert ex._collection is None

    def test_remove_not_present_raises(self, collection):
        ex = FakeExhibitForCollection("EX-001")
        with pytest.raises(ValueError):
            collection.remove_exhibit(ex)


class TestCollectionFindExhibit:
    def test_find_success(self, collection_with_exhibits):
        found = collection_with_exhibits.find_exhibit("EX-002")
        assert found.title == "Girl with a Pearl Earring"

    def test_find_not_found_raises(self, collection_with_exhibits):
        with pytest.raises(ExhibitNotFoundException):
            collection_with_exhibits.find_exhibit("EX-999")

    def test_find_in_empty_collection_raises(self, collection):
        with pytest.raises(ExhibitNotFoundException):
            collection.find_exhibit("EX-001")


class TestCollectionCount:
    def test_count_empty(self, collection):
        assert collection.count_exhibits() == 0

    def test_count_with_items(self, collection_with_exhibits):
        assert collection_with_exhibits.count_exhibits() == 3


class TestCollectionTotalValue:
    def test_total_value_empty(self, collection):
        assert collection.calculate_total_value() == 0

    def test_total_value_with_items(self, collection_with_exhibits):
        # 5000 + 3000 + 1000 = 9000
        assert collection_with_exhibits.calculate_total_value() == 9000.0


class TestCollectionAvailableForExhibition:
    def test_returns_only_available(self, collection_with_exhibits):
        available = collection_with_exhibits.available_for_exhibition()
        # EX-003 has available=False
        assert len(available) == 2
        assert all(ex.inventory_number != "EX-003" for ex in available)

    def test_empty_collection(self, collection):
        assert collection.available_for_exhibition() == []


class TestDigitalCopyInit:
    def test_init_stores_fields(self, digital_copy, fake_source):
        assert digital_copy.source is fake_source
        assert digital_copy.format == "jpg"
        assert digital_copy.size == 1024
        assert digital_copy.resolution == "300dpi"

    def test_init_not_created(self, digital_copy):
        assert digital_copy.is_created is False
        assert digital_copy.path is None

    def test_init_not_published(self, digital_copy):
        assert digital_copy.is_published is False

    def test_init_none_source_raises(self):
        from museum_exhibits.DigitalCopy import DigitalCopy
        with pytest.raises(ValueError):
            DigitalCopy(None, "jpg", 100, "300dpi")

    def test_init_empty_format_raises(self, fake_source):
        from museum_exhibits.DigitalCopy import DigitalCopy
        with pytest.raises(ValueError):
            DigitalCopy(fake_source, "", 100, "300dpi")

    def test_init_empty_resolution_raises(self, fake_source):
        from museum_exhibits.DigitalCopy import DigitalCopy
        with pytest.raises(ValueError):
            DigitalCopy(fake_source, "jpg", 100, "")

    def test_init_negative_size_raises(self, fake_source):
        from museum_exhibits.DigitalCopy import DigitalCopy
        with pytest.raises(ValueError):
            DigitalCopy(fake_source, "jpg", -1, "300dpi")

    def test_init_zero_size_allowed(self, fake_source):
        from museum_exhibits.DigitalCopy import DigitalCopy
        dc = DigitalCopy(fake_source, "jpg", 0, "300dpi")
        assert dc.size == 0


class TestDigitalCopyCreate:
    def test_create_success(self, digital_copy):
        result = digital_copy.create()
        assert result is True
        assert digital_copy.is_created is True
        assert digital_copy.path == "/digital/EX-001.jpg"

    def test_create_idempotent(self, digital_copy_created):
        """Creating an already created copy is not an error."""
        result = digital_copy_created.create()
        assert result is True
        assert digital_copy_created.is_created is True

    def test_create_does_not_overwrite_path(self, digital_copy_created):
        """Calling create twice keeps the same path."""
        old_path = digital_copy_created.path
        digital_copy_created.create()
        assert digital_copy_created.path == old_path


class TestDigitalCopyStore:
    def test_store_without_path(self, digital_copy_created):
        result = digital_copy_created.store()
        assert result is True
        assert digital_copy_created.path == "/digital/EX-001.jpg"

    def test_store_with_new_path(self, digital_copy_created):
        result = digital_copy_created.store("/archive/copy.jpg")
        assert result is True
        assert digital_copy_created.path == "/archive/copy.jpg"

    def test_store_not_created_raises(self, digital_copy):
        from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
        with pytest.raises(InvalidExhibitStateException):
            digital_copy.store()


class TestDigitalCopyPublish:
    def test_publish_success(self, digital_copy_created):
        result = digital_copy_created.publish_to_website()
        assert result is True
        assert digital_copy_created.is_published is True

    def test_publish_idempotent(self, digital_copy_created):
        digital_copy_created.publish_to_website()
        result = digital_copy_created.publish_to_website()
        assert result is True
        assert digital_copy_created.is_published is True

    def test_publish_not_created_raises(self, digital_copy):
        from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
        with pytest.raises(InvalidExhibitStateException):
            digital_copy.publish_to_website()


class TestDigitalCopyUnpublish:
    def test_unpublish_success(self, digital_copy_created):
        digital_copy_created.publish_to_website()
        result = digital_copy_created.unpublish()
        assert result is True
        assert digital_copy_created.is_published is False

    def test_unpublish_idempotent(self, digital_copy_created):
        """Unpublishing a never-published copy is not an error."""
        result = digital_copy_created.unpublish()
        assert result is True
        assert digital_copy_created.is_published is False


class TestDigitalCopyConvert:
    def test_convert_success(self, digital_copy_created):
        result = digital_copy_created.convert("pdf")
        assert result is True
        assert digital_copy_created.format == "pdf"
        assert digital_copy_created.path == "/digital/EX-001.pdf"

    def test_convert_same_format_raises(self, digital_copy_created):
        with pytest.raises(ValueError):
            digital_copy_created.convert("jpg")

    def test_convert_empty_format_raises(self, digital_copy_created):
        with pytest.raises(ValueError):
            digital_copy_created.convert("")

    def test_convert_not_created_raises(self, digital_copy):
        from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
        with pytest.raises(InvalidExhibitStateException):
            digital_copy.convert("pdf")

    def test_convert_multiple_times(self, digital_copy_created):
        digital_copy_created.convert("pdf")
        digital_copy_created.convert("tiff")
        assert digital_copy_created.format == "tiff"
        assert digital_copy_created.path == "/digital/EX-001.tiff"


class TestDigitalCopyGetInfo:
    def test_get_info_before_create(self, digital_copy):
        info = digital_copy.get_info()
        assert info["source"] == "EX-001"
        assert info["format"] == "jpg"
        assert info["size"] == 1024
        assert info["resolution"] == "300dpi"
        assert info["path"] is None
        assert info["published"] is False

    def test_get_info_after_create_and_publish(self, digital_copy_created):
        digital_copy_created.publish_to_website()
        info = digital_copy_created.get_info()
        assert info["path"] == "/digital/EX-001.jpg"
        assert info["published"] is True


class TestDocumentInit:
    def test_init_stores_fields(self, document):
        assert document.title == "Codex Sinaiticus"
        assert document.author == "Unknown"
        assert document.doc_type == "manuscript"
        assert document.pages == 346
        assert document.language == "grc"

    def test_init_not_digitized(self, document):
        assert document.is_digitized is False
        assert document.digital_copy is None

    def test_init_neutral_acidity(self, document):
        assert document.acidity_level == 7.0
        assert document.check_acidity() == "neutral"

    def test_init_empty_doc_type_raises(self):
        from museum_exhibits.Document import Document
        with pytest.raises(ValueError):
            Document("T", "A", "", 10, "en")

    def test_init_negative_pages_raises(self):
        from museum_exhibits.Document import Document
        with pytest.raises(ValueError):
            Document("T", "A", "book", -1, "en")

    def test_init_empty_language_raises(self):
        from museum_exhibits.Document import Document
        with pytest.raises(ValueError):
            Document("T", "A", "book", 10, "")

    def test_init_zero_pages_allowed(self):
        from museum_exhibits.Document import Document
        d = Document("T", "A", "letter", 0, "en")
        assert d.pages == 0


class TestDocumentDigitize:
    def test_digitize_success(self, document):
        copy = document.digitize()
        assert copy is not None
        assert document.is_digitized is True
        assert document.digital_copy is copy

    def test_digitize_creates_created_copy(self, document):
        copy = document.digitize()
        assert copy.is_created is True
        assert copy.source is document
        assert copy.format == "pdf"

    def test_digitize_idempotent_returns_same_copy(self, document):
        """Second call returns the same DigitalCopy, not a new one."""
        first = document.digitize()
        second = document.digitize()
        assert first is second

    def test_digitize_does_not_create_duplicate(self, document):
        first = document.digitize()
        second = document.digitize()
        assert first is document.digital_copy
        assert second is document.digital_copy


class TestDocumentAcidity:
    def test_neutral_acidity(self, document):
        assert document.check_acidity() == "neutral"

    def test_acidic_acidity(self, document_acidic):
        assert document_acidic.acidity_level == 4.0
        assert document_acidic.check_acidity() == "acidic"

    def test_alkaline_acidity(self, document):
        document.set_acidity_level(9.0)
        assert document.check_acidity() == "alkaline"


class TestDocumentSetAcidityLevel:
    def test_set_success(self, document):
        assert document.set_acidity_level(6.0) is True
        assert document.acidity_level == 6.0

    def test_set_at_min_boundary(self, document):
        assert document.set_acidity_level(0.0) is True

    def test_set_at_max_boundary(self, document):
        assert document.set_acidity_level(14.0) is True

    def test_set_below_min_raises(self, document):
        with pytest.raises(ValueError):
            document.set_acidity_level(-1.0)

    def test_set_above_max_raises(self, document):
        with pytest.raises(ValueError):
            document.set_acidity_level(15.0)


class TestDocumentIsFragile:
    def test_good_condition_neutral_not_fragile(self, document):
        assert document.is_fragile() is False

    def test_acidic_is_fragile(self, document_acidic):
        assert document_acidic.is_fragile() is True

    def test_critical_condition_is_fragile(self, document_critical):
        assert document_critical.is_fragile() is True

    def test_critical_with_neutral_acidity_is_fragile(self, document_critical):
        # condition critical, acidity 7.0
        assert document_critical.acidity_level == 7.0
        assert document_critical.is_fragile() is True

    def test_acidic_but_good_condition_is_fragile(self, document):
        document.set_acidity_level(3.0)
        assert document.is_fragile() is True


class TestExhibitInit:
    def test_init_stores_fields(self, exhibit):
        assert exhibit.title == "Mona Lisa"
        assert exhibit.author == "Leonardo da Vinci"
        assert exhibit.condition == "good"

    def test_init_generates_inventory_number(self, exhibit):
        assert exhibit.inventory_number.startswith("EX-")
        assert len(exhibit.inventory_number) == 9  # EX-000001

    def test_init_inventory_numbers_are_unique(self):
        from museum_exhibits.Exhibit import Exhibit
        e1 = Exhibit("A", "B")
        e2 = Exhibit("C", "D")
        assert e1.inventory_number != e2.inventory_number

    def test_init_no_collection(self, exhibit):
        assert exhibit.collection is None

    def test_init_no_location(self, exhibit):
        assert exhibit.location is None

    def test_init_no_insurance(self, exhibit):
        assert exhibit.insurance_value == 0.0
        assert exhibit.insurance_policy is None

    def test_init_no_acquired_date(self, exhibit):
        assert exhibit.acquired_date is None

    def test_init_empty_title_raises(self):
        from museum_exhibits.Exhibit import Exhibit
        with pytest.raises(ValueError):
            Exhibit("", "Author")

    def test_init_empty_author_raises(self):
        from museum_exhibits.Exhibit import Exhibit
        with pytest.raises(ValueError):
            Exhibit("Title", "")

    def test_init_invalid_condition_raises(self):
        from museum_exhibits.Exhibit import Exhibit
        with pytest.raises(ValueError):
            Exhibit("Title", "Author", condition="broken")


class TestExhibitMoveTo:
    def test_move_to_success(self, exhibit, fake_location_a):
        result = exhibit.move_to(fake_location_a)
        assert result is True
        assert exhibit.location is fake_location_a

    def test_move_to_none_raises(self, exhibit):
        with pytest.raises(ValueError):
            exhibit.move_to(None)

    def test_move_to_same_location_idempotent(self, exhibit, fake_location_a):
        exhibit.move_to(fake_location_a)
        result = exhibit.move_to(fake_location_a)
        assert result is True
        assert exhibit.location is fake_location_a

    def test_move_to_different_location_updates(self, exhibit, fake_location_a, fake_location_b):
        exhibit.move_to(fake_location_a)
        exhibit.move_to(fake_location_b)
        assert exhibit.location is fake_location_b


class TestExhibitRemoveFromLocation:
    def test_remove_success(self, exhibit, fake_location_a):
        exhibit.move_to(fake_location_a)
        result = exhibit.remove_from_location()
        assert result is True
        assert exhibit.location is None

    def test_remove_idempotent(self, exhibit):
        """Removing when there is no location is not an error."""
        result = exhibit.remove_from_location()
        assert result is True
        assert exhibit.location is None


class TestExhibitAttachToCollection:
    def test_attach_success(self, exhibit, fake_collection_a):
        result = exhibit.attach_to_collection(fake_collection_a)
        assert result is True
        assert exhibit.collection is fake_collection_a

    def test_attach_none_raises(self, exhibit):
        with pytest.raises(ValueError):
            exhibit.attach_to_collection(None)

    def test_attach_same_collection_idempotent(self, exhibit, fake_collection_a):
        exhibit.attach_to_collection(fake_collection_a)
        result = exhibit.attach_to_collection(fake_collection_a)
        assert result is True
        assert exhibit.collection is fake_collection_a

    def test_attach_different_collection_raises(self, exhibit, fake_collection_a, fake_collection_b):
        from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
        exhibit.attach_to_collection(fake_collection_a)
        with pytest.raises(InvalidExhibitStateException):
            exhibit.attach_to_collection(fake_collection_b)


class TestExhibitRemoveFromCollection:
    def test_remove_success(self, exhibit, fake_collection_a):
        exhibit.attach_to_collection(fake_collection_a)
        result = exhibit.remove_from_collection()
        assert result is True
        assert exhibit.collection is None

    def test_remove_idempotent(self, exhibit):
        result = exhibit.remove_from_collection()
        assert result is True
        assert exhibit.collection is None

    def test_reattach_after_remove(self, exhibit, fake_collection_a, fake_collection_b):
        """After detach, exhibit can be attached to a different collection."""
        exhibit.attach_to_collection(fake_collection_a)
        exhibit.remove_from_collection()
        assert exhibit.attach_to_collection(fake_collection_b) is True
        assert exhibit.collection is fake_collection_b


class TestExhibitUpdateCondition:
    def test_update_to_damaged(self, exhibit):
        result = exhibit.update_condition("damaged")
        assert result is True
        assert exhibit.condition == "damaged"

    def test_update_to_critical(self, exhibit):
        exhibit.update_condition("critical")
        assert exhibit.condition == "critical"

    def test_update_to_excellent(self, exhibit_damaged):
        exhibit_damaged.update_condition("excellent")
        assert exhibit_damaged.condition == "excellent"

    def test_update_invalid_condition_raises(self, exhibit):
        with pytest.raises(ValueError):
            exhibit.update_condition("broken")

    def test_update_empty_string_raises(self, exhibit):
        with pytest.raises(ValueError):
            exhibit.update_condition("")


class TestExhibitNeedsRestoration:
    def test_good_does_not_need(self, exhibit):
        assert exhibit.needs_restoration() is False

    def test_excellent_does_not_need(self):
        from museum_exhibits.Exhibit import Exhibit
        e = Exhibit("T", "A", condition="excellent")
        assert e.needs_restoration() is False

    def test_damaged_needs(self, exhibit_damaged):
        assert exhibit_damaged.needs_restoration() is True

    def test_critical_needs(self, exhibit_critical):
        assert exhibit_critical.needs_restoration() is True


class TestExhibitIsAvailableForExhibition:
    def test_good_available(self, exhibit):
        assert exhibit.is_available_for_exhibition() is True

    def test_excellent_available(self):
        from museum_exhibits.Exhibit import Exhibit
        e = Exhibit("T", "A", condition="excellent")
        assert e.is_available_for_exhibition() is True

    def test_damaged_available(self, exhibit_damaged):
        assert exhibit_damaged.is_available_for_exhibition() is True

    def test_critical_not_available(self, exhibit_critical):
        assert exhibit_critical.is_available_for_exhibition() is False


class TestExhibitInsuranceValue:
    def test_set_value_success(self, exhibit):
        result = exhibit.set_insurance_value(5000.0)
        assert result is True
        assert exhibit.insurance_value == 5000.0

    def test_set_zero_allowed(self, exhibit):
        assert exhibit.set_insurance_value(0.0) is True

    def test_set_negative_raises(self, exhibit):
        with pytest.raises(ValueError):
            exhibit.set_insurance_value(-100.0)


class TestExhibitEvaluateInsurance:
    def test_evaluate_good(self, exhibit):
        # good -> multiplier 1.0
        value = exhibit.evaluate_insurance(1000.0)
        assert value == 1000.0
        assert exhibit.insurance_value == 1000.0

    def test_evaluate_excellent(self):
        from museum_exhibits.Exhibit import Exhibit
        e = Exhibit("T", "A", condition="excellent")
        assert e.evaluate_insurance(1000.0) == 1500.0

    def test_evaluate_damaged(self, exhibit_damaged):
        assert exhibit_damaged.evaluate_insurance(1000.0) == 500.0

    def test_evaluate_critical(self, exhibit_critical):
        assert exhibit_critical.evaluate_insurance(1000.0) == 200.0


class TestExhibitInsurancePolicy:
    def test_attach_policy_success(self, exhibit, fake_policy):
        result = exhibit.attach_insurance_policy(fake_policy)
        assert result is True
        assert exhibit.insurance_policy is fake_policy

    def test_has_insurance_false_by_default(self, exhibit):
        assert exhibit.insurance_policy is None

    def test_attach_none_raises(self, exhibit):
        with pytest.raises(ValueError):
            exhibit.attach_insurance_policy(None)


class TestExhibitAcquiredDate:
    def test_set_date_success(self, exhibit):
        from datetime import date
        d = date(2020, 5, 15)
        result = exhibit.set_acquired_date(d)
        assert result is True
        assert exhibit.acquired_date == d

    def test_set_none_raises(self, exhibit):
        with pytest.raises(ValueError):
            exhibit.set_acquired_date(None)


class TestExhibitSendToRestoration:
    def test_send_none_restorer_raises(self, exhibit):
        with pytest.raises(ValueError):
            exhibit.send_to_restoration(None)


class TestFundInit:
    def test_init_stores_fields(self, fund_painting):
        assert fund_painting.name == "Painting Fund"
        assert fund_painting.type == "painting"

    def test_init_collections_empty(self, fund_painting):
        assert fund_painting.collections == []

    def test_init_written_off_empty(self, fund_painting):
        assert fund_painting.written_off == []

    def test_init_empty_name_raises(self):
        from museum_exhibits.Fund import Fund
        with pytest.raises(ValueError):
            Fund("", Fund.TYPE_PAINTING)

    def test_init_invalid_type_raises(self):
        from museum_exhibits.Fund import Fund
        with pytest.raises(ValueError):
            Fund("Some Fund", "unknown")

    def test_init_all_valid_types(self):
        from museum_exhibits.Fund import Fund
        for t in ("painting", "sculpture", "document", "mixed"):
            f = Fund("F", t)
            assert f.type == t


class TestFundAddCollection:
    def test_add_success(self, fund_painting, collection):
        result = fund_painting.add_collection(collection)
        assert result is True
        assert collection in fund_painting.collections

    def test_add_none_raises(self, fund_painting):
        with pytest.raises(ValueError):
            fund_painting.add_collection(None)

    def test_add_duplicate_raises(self, fund_painting, collection):
        fund_painting.add_collection(collection)
        with pytest.raises(ValueError):
            fund_painting.add_collection(collection)


class TestFundRemoveCollection:
    def test_remove_success(self, fund_painting, collection):
        fund_painting.add_collection(collection)
        result = fund_painting.remove_collection(collection)
        assert result is True
        assert collection not in fund_painting.collections

    def test_remove_not_present_raises(self, fund_painting, collection):
        with pytest.raises(ValueError):
            fund_painting.remove_collection(collection)


class TestFundFindCollection:
    def test_find_success(self, fund_painting, collection):
        fund_painting.add_collection(collection)
        found = fund_painting.find_collection("Dutch Golden Age")
        assert found is collection

    def test_find_not_found_raises(self, fund_painting):
        with pytest.raises(ValueError):
            fund_painting.find_collection("Nonexistent")

    def test_find_in_empty_fund_raises(self, fund_painting):
        with pytest.raises(ValueError):
            fund_painting.find_collection("Any")


class TestFundAcceptItem:
    def test_accept_painting_into_painting_fund(self, fund_with_collection, painting):
        result = fund_with_collection.accept_item(painting)
        assert result is True
        assert painting in fund_with_collection.collections[0].exhibits

    def test_accept_none_raises(self, fund_with_collection):
        with pytest.raises(ValueError):
            fund_with_collection.accept_item(None)

    def test_accept_wrong_type_raises(self, fund_with_collection, sculpture):
        """A painting fund should not accept a sculpture."""
        with pytest.raises(ValueError):
            fund_with_collection.accept_item(sculpture)

    def test_accept_into_mixed_fund(self, fund_mixed, collection, painting):
        fund_mixed.add_collection(collection)
        result = fund_mixed.accept_item(painting)
        assert result is True

    def test_accept_mixed_fund_sculpture_accepted(self, fund_mixed, collection, sculpture):
        """Mixed fund accepts sculptures too."""
        fund_mixed.add_collection(collection)
        result = fund_mixed.accept_item(sculpture)
        assert result is True

    def test_accept_no_collections_raises(self, fund_painting, painting):
        from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
        with pytest.raises(InvalidExhibitStateException):
            fund_painting.accept_item(painting)

    def test_accept_already_in_other_collection_raises(self, fund_with_collection, painting, collection):
        from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
        from museum_exhibits.Collection import Collection
        other = Collection("Other", "theme")
        other.add_exhibit(painting)
        with pytest.raises(InvalidExhibitStateException):
            fund_with_collection.accept_item(painting)

class TestFundWriteOffItem:
    def test_write_off_success(self, fund_with_collection, painting):
        fund_with_collection.accept_item(painting)
        result = fund_with_collection.write_off_item(painting)
        assert result is True
        assert painting in fund_with_collection.written_off
        assert painting not in fund_with_collection.collections[0].exhibits

    def test_write_off_none_raises(self, fund_with_collection):
        with pytest.raises(ValueError):
            fund_with_collection.write_off_item(None)

    def test_write_off_not_in_fund_raises(self, fund_with_collection, painting):
        with pytest.raises(ValueError):
            fund_with_collection.write_off_item(painting)

    def test_write_off_twice_raises(self, fund_with_collection, painting):
        fund_with_collection.accept_item(painting)
        fund_with_collection.write_off_item(painting)
        with pytest.raises(ValueError):
            fund_with_collection.write_off_item(painting)

class TestFundCountExhibits:
    def test_count_empty(self, fund_painting):
        assert fund_painting.count_exhibits() == 0

    def test_count_after_accept(self, fund_with_collection, painting):
        fund_with_collection.accept_item(painting)
        assert fund_with_collection.count_exhibits() == 1


class TestFundTotalValue:
    def test_total_value_empty(self, fund_painting):
        assert fund_painting.total_value() == 0

    def test_total_value_after_accept(self, fund_with_collection, painting):
        fund_with_collection.accept_item(painting)
        # painting has default insurance_value = 0.0
        assert fund_with_collection.total_value() == 0.0


class TestFundGenerateReport:
    def test_report_empty(self, fund_painting):
        report = fund_painting.generate_report()
        assert report["fund"] == "Painting Fund"
        assert report["type"] == "painting"
        assert report["collections"] == 0
        assert report["exhibits"] == 0
        assert report["total_value"] == 0
        assert report["written_off"] == 0

    def test_report_after_accept(self, fund_with_collection, painting):
        fund_with_collection.accept_item(painting)
        report = fund_with_collection.generate_report()
        assert report["collections"] == 1
        assert report["exhibits"] == 1
        assert report["total_value"] == 0.0


class TestFundNeedsRestoration:
    def test_needs_restoration_empty(self, fund_painting):
        assert fund_painting.needs_restoration() == []

    def test_needs_restoration_finds_damaged(self, fund_with_collection, painting_damaged):
        fund_with_collection.accept_item(painting_damaged)
        result = fund_with_collection.needs_restoration()
        assert painting_damaged in result

    def test_needs_restoration_ignores_good(self, fund_with_collection, painting):
        fund_with_collection.accept_item(painting)
        # painting is "excellent" — not damaged, not critical
        assert fund_with_collection.needs_restoration() == []

    def test_needs_restoration_multiple(self, fund_with_collection, painting, painting_damaged):
        fund_with_collection.accept_item(painting)
        fund_with_collection.accept_item(painting_damaged)
        result = fund_with_collection.needs_restoration()
        assert painting not in result
        assert painting_damaged in result

class TestPaintingInit:
    def test_init_stores_fields(self, painting):
        assert painting.title == "Night Watch"
        assert painting.author == "Rembrandt"
        assert painting.technique == "oil"
        assert painting.width == 3.6
        assert painting.height == 4.4
        assert painting.condition == "excellent"

    def test_init_no_frame(self, painting):
        assert painting.frame is None

    def test_init_no_varnish(self, painting):
        assert painting.has_varnish is False

    def test_init_inherits_inventory_number(self, painting):
        assert painting.inventory_number.startswith("EX-")

    def test_init_empty_technique_raises(self):
        from museum_exhibits.Painting import Painting
        with pytest.raises(ValueError):
            Painting("T", "A", "", 1.0, 1.0)

    def test_init_zero_width_raises(self):
        from museum_exhibits.Painting import Painting
        with pytest.raises(ValueError):
            Painting("T", "A", "oil", 0.0, 1.0)

    def test_init_negative_height_raises(self):
        from museum_exhibits.Painting import Painting
        with pytest.raises(ValueError):
            Painting("T", "A", "oil", 1.0, -1.0)


class TestPaintingArea:
    def test_area(self, painting):
        # 3.6 * 4.4 = 15.84
        assert abs(painting.area() - 15.84) < 1e-9


class TestPaintingFrame:
    def test_set_frame_success(self, painting):
        result = painting.set_frame("Gold wooden frame")
        assert result is True
        assert painting.frame == "Gold wooden frame"

    def test_set_empty_frame_raises(self, painting):
        with pytest.raises(ValueError):
            painting.set_frame("")


class TestPaintingVarnish:
    def test_apply_varnish_success(self, painting):
        assert painting.apply_varnish() is True
        assert painting.has_varnish is True

    def test_apply_varnish_idempotent(self, painting):
        painting.apply_varnish()
        assert painting.apply_varnish() is True
        assert painting.has_varnish is True


class TestPaintingRestorationCost:
    def test_estimate_cost(self, painting):
        # area * 500 = 15.84 * 500 = 7920
        cost = painting.estimate_restoration_cost()
        assert abs(cost - 7920.0) < 1e-6

    def test_estimate_cost_scales_with_area(self, painting):
        from museum_exhibits.Painting import Painting
        small = Painting("S", "A", "oil", width=1.0, height=1.0)
        assert small.estimate_restoration_cost() == 500.0


class TestPaintingInheritsExhibit:
    def test_has_needs_restoration(self, painting):
        assert painting.needs_restoration() is False

    def test_inherits_move_to(self, painting, fake_location_a):
        painting.move_to(fake_location_a)
        assert painting.location is fake_location_a


class TestSculptureInit:
    def test_init_stores_fields(self, sculpture):
        assert sculpture.title == "David"
        assert sculpture.author == "Michelangelo"
        assert sculpture.material == "marble"
        assert sculpture.height == 5.17
        assert sculpture.weight == 5660.0

    def test_init_not_marked_for_reinforcement(self, sculpture):
        assert sculpture.needs_reinforcement is False

    def test_init_base_ok(self, sculpture):
        assert sculpture.base_condition == "ok"

    def test_init_empty_material_raises(self):
        from museum_exhibits.Sculpture import Sculpture
        with pytest.raises(ValueError):
            Sculpture("T", "A", "", 1.0, 10.0)

    def test_init_zero_height_raises(self):
        from museum_exhibits.Sculpture import Sculpture
        with pytest.raises(ValueError):
            Sculpture("T", "A", "marble", 0.0, 10.0)

    def test_init_negative_weight_raises(self):
        from museum_exhibits.Sculpture import Sculpture
        with pytest.raises(ValueError):
            Sculpture("T", "A", "marble", 1.0, -1.0)


class TestSculptureReinforcement:
    def test_mark_for_reinforcement_success(self, sculpture):
        assert sculpture.mark_for_reinforcement() is True
        assert sculpture.needs_reinforcement is True

    def test_mark_for_reinforcement_idempotent(self, sculpture):
        sculpture.mark_for_reinforcement()
        assert sculpture.mark_for_reinforcement() is True
        assert sculpture.needs_reinforcement is True

    def test_reinforce_base_success(self, sculpture):
        sculpture.mark_for_reinforcement()
        result = sculpture.reinforce_base()
        assert result is True
        assert sculpture.needs_reinforcement is False
        assert sculpture.base_condition == "reinforced"

    def test_reinforce_base_without_flag_raises(self, sculpture):
        with pytest.raises(ValueError):
            sculpture.reinforce_base()


class TestSculptureInheritsExhibit:
    def test_has_needs_restoration(self, sculpture):
        assert sculpture.needs_restoration() is False

    def test_inherits_update_condition(self, sculpture):
        sculpture.update_condition("damaged")
        assert sculpture.condition == "damaged"
        assert sculpture.needs_restoration() is True

    def test_inherits_is_available_for_exhibition(self, sculpture):
        assert sculpture.is_available_for_exhibition() is True

    def test_inherits_move_to(self, sculpture, fake_location_a):
        sculpture.move_to(fake_location_a)
        assert sculpture.location is fake_location_a