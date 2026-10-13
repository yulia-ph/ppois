"""Tests for the museum_exhibitions package.

Covers: Exhibition, TemporaryExhibition, PermanentExhibition, Excursion.
"""
from datetime import date, datetime, timedelta

import pytest

from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
from museum_exhibitions.Excursion import Excursion
from museum_exhibitions.Exhibition import Exhibition
from museum_exhibitions.PermanentExhibition import PermanentExhibition
from museum_exhibitions.TemporaryExhibition import TemporaryExhibition


class TestExhibitionInit:
    def test_init_stores_fields(self, exhibition, curator):
        assert exhibition.title == "Impressionists"
        assert exhibition.curator is curator
        assert exhibition.start_date == date(2025, 1, 1)
        assert exhibition.end_date == date(2025, 12, 31)

    def test_init_has_id(self, exhibition):
        assert exhibition.id.startswith("EXH-")

    def test_init_ids_are_unique(self, curator):
        e1 = Exhibition("A", date(2025, 1, 1), date(2025, 12, 31), curator)
        e2 = Exhibition("B", date(2025, 1, 1), date(2025, 12, 31), curator)
        assert e1.id != e2.id

    def test_init_not_open(self, exhibition):
        assert exhibition.is_open is False

    def test_init_empty_collections(self, exhibition):
        assert exhibition.exhibits == []
        assert exhibition.tickets == []

    def test_init_default_type_permanent(self, exhibition):
        assert exhibition.type == "permanent"

    def test_init_all_valid_types(self, curator):
        for t in ("permanent", "temporary", "mixed"):
            e = Exhibition("T", date(2025, 1, 1), date(2025, 12, 31),
                           curator, type_=t)
            assert e.type == t

    def test_init_empty_title_raises(self, curator):
        with pytest.raises(ValueError):
            Exhibition("", date(2025, 1, 1), date(2025, 12, 31), curator)

    def test_init_none_start_raises(self, curator):
        with pytest.raises(ValueError):
            Exhibition("X", None, date(2025, 12, 31), curator)

    def test_init_none_end_raises(self, curator):
        with pytest.raises(ValueError):
            Exhibition("X", date(2025, 1, 1), None, curator)

    def test_init_end_before_start_raises(self, curator):
        with pytest.raises(ValueError):
            Exhibition("X", date(2025, 12, 31), date(2025, 1, 1), curator)

    def test_init_end_equals_start_raises(self, curator):
        d = date(2025, 6, 1)
        with pytest.raises(ValueError):
            Exhibition("X", d, d, curator)

    def test_init_none_curator_raises(self):
        with pytest.raises(ValueError):
            Exhibition("X", date(2025, 1, 1), date(2025, 12, 31), None)

    def test_init_invalid_type_raises(self, curator):
        with pytest.raises(ValueError):
            Exhibition("X", date(2025, 1, 1), date(2025, 12, 31), curator,
                       type_="popup")


class TestExhibitionAddExhibit:
    def test_add_success(self, exhibition, painting):
        result = exhibition.add_exhibit(painting)
        assert result is True
        assert painting in exhibition.exhibits

    def test_add_none_raises(self, exhibition):
        with pytest.raises(ValueError):
            exhibition.add_exhibit(None)

    def test_add_duplicate_raises(self, exhibition, painting):
        exhibition.add_exhibit(painting)
        with pytest.raises(ValueError):
            exhibition.add_exhibit(painting)

    def test_add_critical_exhibit_raises(self, exhibition):
        from museum_exhibits.Exhibit import Exhibit
        critical = Exhibit("Ruined", "Unknown", condition="critical")
        with pytest.raises(InvalidExhibitStateException):
            exhibition.add_exhibit(critical)

    def test_add_damaged_exhibit_ok(self, exhibition, painting_damaged):
        # damaged is still available for exhibition
        assert exhibition.add_exhibit(painting_damaged) is True


class TestExhibitionCountExhibits:
    def test_count_empty(self, exhibition):
        assert exhibition.count_exhibits() == 0

    def test_count_after_add(self, exhibition, painting):
        exhibition.add_exhibit(painting)
        assert exhibition.count_exhibits() == 1


class TestExhibitionLifecycle:
    def test_open_success(self, exhibition):
        assert exhibition.open() is True
        assert exhibition.is_open is True

    def test_open_idempotent(self, exhibition):
        exhibition.open()
        assert exhibition.open() is True
        assert exhibition.is_open is True

    def test_close_success(self, exhibition_open):
        assert exhibition_open.close() is True
        assert exhibition_open.is_open is False

    def test_close_idempotent(self, exhibition):
        assert exhibition.close() is True
        assert exhibition.is_open is False


class TestExhibitionExtendDates:
    def test_extend_success(self, exhibition):
        new_end = date(2026, 6, 30)
        assert exhibition.extend_dates(new_end) is True
        assert exhibition.end_date == new_end

    def test_extend_same_date_raises(self, exhibition):
        with pytest.raises(ValueError):
            exhibition.extend_dates(exhibition.end_date)

    def test_extend_earlier_raises(self, exhibition):
        with pytest.raises(ValueError):
            exhibition.extend_dates(date(2025, 1, 1))

    def test_extend_none_raises(self, exhibition):
        with pytest.raises(ValueError):
            exhibition.extend_dates(None)


class TestExhibitionDuration:
    def test_duration_days(self, exhibition):
        # 2025-01-01 to 2025-12-31 = 364 days
        assert exhibition.duration_days() == 364


class TestExhibitionTickets:
    def test_add_success(self, exhibition, ticket):
        result = exhibition.add_ticket(ticket)
        assert result is True
        assert ticket in exhibition.tickets

    def test_add_none_raises(self, exhibition):
        with pytest.raises(ValueError):
            exhibition.add_ticket(None)

    def test_add_duplicate_raises(self, exhibition, ticket):
        exhibition.add_ticket(ticket)
        with pytest.raises(ValueError):
            exhibition.add_ticket(ticket)

    def test_calculate_tickets_sold(self, exhibition, adult_ticket_type):
        from museum_sales.Ticket import Ticket
        for _ in range(3):
            exhibition.add_ticket(Ticket(adult_ticket_type, date.today()))
        assert exhibition.calculate_tickets_sold() == 3

    def test_calculate_revenue(self, exhibition, adult_ticket_type):
        from museum_sales.Ticket import Ticket
        for _ in range(3):
            exhibition.add_ticket(Ticket(adult_ticket_type, date.today()))
        # 3 * 500 = 1500
        assert exhibition.calculate_revenue() == 1500.0


class TestExhibitionChangeCurator:
    def test_change_success(self, exhibition):
        class FakeCurator:
            def __init__(self, name):
                self.name = name
        new = FakeCurator("New Curator")
        assert exhibition.change_curator(new) is True
        assert exhibition.curator is new

    def test_change_none_raises(self, exhibition):
        with pytest.raises(ValueError):
            exhibition.change_curator(None)

    def test_change_when_open_raises(self, exhibition_open):
        class FakeCurator:
            name = "New"
        with pytest.raises(InvalidExhibitStateException):
            exhibition_open.change_curator(FakeCurator())


class TestExhibitionEncapsulation:
    def test_exhibits_returns_copy(self, exhibition, painting):
        exhibition.add_exhibit(painting)
        exs = exhibition.exhibits
        exs.append("fake")
        assert exhibition.count_exhibits() == 1

    def test_tickets_returns_copy(self, exhibition, ticket):
        exhibition.add_ticket(ticket)
        tks = exhibition.tickets
        tks.append("fake")
        assert exhibition.calculate_tickets_sold() == 1


class TestTemporaryExhibitionInit:
    def test_init_stores_theme(self, temporary_exhibition):
        assert temporary_exhibition.theme == "post-impressionism"

    def test_init_type_is_temporary(self, temporary_exhibition):
        assert temporary_exhibition.type == "temporary"

    def test_init_no_loans(self, temporary_exhibition):
        assert temporary_exhibition.loans == []

    def test_init_empty_theme_raises(self, curator):
        with pytest.raises(ValueError):
            TemporaryExhibition("T", date(2025, 1, 1), date(2025, 12, 31),
                                curator, theme="")

    def test_inherits_validation(self, curator):
        with pytest.raises(ValueError):
            TemporaryExhibition("", date(2025, 1, 1), date(2025, 12, 31),
                                curator, theme="x")


class TestTemporaryExhibitionLoans:
    def test_add_success(self, temporary_exhibition, fake_loan_for_exhibition):
        result = temporary_exhibition.add_loan(fake_loan_for_exhibition)
        assert result is True
        assert fake_loan_for_exhibition in temporary_exhibition.loans

    def test_add_none_raises(self, temporary_exhibition):
        with pytest.raises(ValueError):
            temporary_exhibition.add_loan(None)

    def test_add_duplicate_raises(self, temporary_exhibition, fake_loan_for_exhibition):
        temporary_exhibition.add_loan(fake_loan_for_exhibition)
        with pytest.raises(ValueError):
            temporary_exhibition.add_loan(fake_loan_for_exhibition)

    def test_return_loans_returns_count(self, temporary_exhibition):
        class L:
            def __init__(self):
                self.returned = False
            def return_exhibit(self):
                if self.returned:
                    return False
                self.returned = True
                return True
            def is_overdue(self):
                return False
        a, b = L(), L()
        temporary_exhibition.add_loan(a)
        temporary_exhibition.add_loan(b)
        assert temporary_exhibition.return_loans() == 2

    def test_return_loans_ignores_already_returned(self, temporary_exhibition):
        class L:
            def __init__(self):
                self.returned = False
            def return_exhibit(self):
                if self.returned:
                    return False
                self.returned = True
                return True
            def is_overdue(self):
                return False
        a = L()
        a.returned = True
        temporary_exhibition.add_loan(a)
        assert temporary_exhibition.return_loans() == 0

    def test_check_loans_overdue(self, temporary_exhibition):
        class FakeLoanOverdue:
            def return_exhibit(self): return True
            def is_overdue(self): return True
        overdue = FakeLoanOverdue()
        temporary_exhibition.add_loan(overdue)
        assert overdue in temporary_exhibition.check_loans_overdue()


class TestPermanentExhibitionInit:
    def test_init_stores_description(self, permanent_exhibition):
        assert permanent_exhibition.description == "Permanent Egyptian collection"

    def test_init_type_is_permanent(self, permanent_exhibition):
        assert permanent_exhibition.type == "permanent"

    def test_init_default_rotation(self, permanent_exhibition):
        assert permanent_exhibition.rotation_period_days == 180

    def test_init_last_update_equals_start(self, permanent_exhibition):
        assert permanent_exhibition.last_update == permanent_exhibition.start_date

    def test_init_end_date_far_future(self, permanent_exhibition):
        # start + 10 years
        expected = permanent_exhibition.start_date + timedelta(days=365 * 10)
        assert permanent_exhibition.end_date == expected

    def test_init_empty_description_allowed(self, curator):
        p = PermanentExhibition("T", date(2020, 1, 1), curator)
        assert p.description == ""


class TestPermanentExhibitionDescription:
    def test_update_description(self, permanent_exhibition):
        result = permanent_exhibition.update_description("New text")
        assert result is True
        assert permanent_exhibition.description == "New text"

    def test_update_description_updates_last_update(self, permanent_exhibition):
        permanent_exhibition.update_description("New")
        assert permanent_exhibition.last_update == date.today()

    def test_update_empty_description_raises(self, permanent_exhibition):
        with pytest.raises(ValueError):
            permanent_exhibition.update_description("")


class TestPermanentExhibitionRotation:
    def test_set_rotation_period_success(self, permanent_exhibition):
        assert permanent_exhibition.set_rotation_period(90) is True
        assert permanent_exhibition.rotation_period_days == 90

    def test_set_rotation_period_zero_raises(self, permanent_exhibition):
        with pytest.raises(ValueError):
            permanent_exhibition.set_rotation_period(0)

    def test_set_rotation_period_negative_raises(self, permanent_exhibition):
        with pytest.raises(ValueError):
            permanent_exhibition.set_rotation_period(-1)

    def test_needs_rotation_false_at_start(self, permanent_exhibition):
        # last_update == start_date (2020-01-01). today default is far later.
        # Override today to just after start.
        p = PermanentExhibition("T", date(2025, 1, 1), permanent_exhibition.curator)
        assert p.needs_rotation(date(2025, 1, 10)) is False

    def test_needs_rotation_true_after_period(self, permanent_exhibition):
        p = PermanentExhibition("T", date(2025, 1, 1), permanent_exhibition.curator)
        p.set_rotation_period(180)
        assert p.needs_rotation(date(2025, 8, 1)) is True

    def test_rotate_exhibits_success(self, permanent_exhibition, painting):
        assert permanent_exhibition.rotate_exhibits([painting]) is True
        assert painting in permanent_exhibition.exhibits

    def test_rotate_exhibits_replaces_old(self, permanent_exhibition, painting, painting_damaged):
        permanent_exhibition.add_exhibit(painting)
        permanent_exhibition.rotate_exhibits([painting_damaged])
        assert painting not in permanent_exhibition.exhibits
        assert painting_damaged in permanent_exhibition.exhibits

    def test_rotate_exhibits_empty_raises(self, permanent_exhibition):
        with pytest.raises(ValueError):
            permanent_exhibition.rotate_exhibits([])

    def test_rotate_if_needed_skips_when_recent(self, permanent_exhibition, painting):
        # last_update is start_date (2020-01-01). today is far later, so needs rotation.
        # Let's use a fresh one with recent last_update.
        p = PermanentExhibition("T", date.today(), permanent_exhibition.curator)
        assert p.rotate_if_needed([painting]) is False

    def test_rotate_if_needed_rotates_when_due(self, permanent_exhibition, painting):
        p = PermanentExhibition("T", date.today() - timedelta(days=400),
                                permanent_exhibition.curator)
        assert p.rotate_if_needed([painting]) is True
        assert painting in p.exhibits


class TestExcursionInit:
    def test_init_stores_fields(self, excursion, fake_excursion_guide, sample_hall):
        assert excursion.guide is fake_excursion_guide
        assert sample_hall in excursion.route_points
        assert excursion.duration_minutes == 60

    def test_init_has_id(self, excursion):
        assert excursion.id.startswith("EXC-")

    def test_init_not_started(self, excursion):
        assert excursion.is_started is False
        assert excursion.is_finished is False
        assert excursion.is_active is False

    def test_init_no_visitors(self, excursion):
        assert excursion.visitors == []

    def test_init_none_guide_raises(self, sample_hall):
        with pytest.raises(ValueError):
            Excursion([sample_hall], None, datetime(2025, 6, 1), 60)

    def test_init_none_start_time_raises(self, fake_excursion_guide, sample_hall):
        with pytest.raises(ValueError):
            Excursion([sample_hall], fake_excursion_guide, None, 60)

    def test_init_zero_duration_raises(self, fake_excursion_guide, sample_hall):
        with pytest.raises(ValueError):
            Excursion([sample_hall], fake_excursion_guide,
                      datetime(2025, 6, 1), 0)

    def test_init_negative_duration_raises(self, fake_excursion_guide, sample_hall):
        with pytest.raises(ValueError):
            Excursion([sample_hall], fake_excursion_guide,
                      datetime(2025, 6, 1), -5)

    def test_init_empty_route_allowed(self, fake_excursion_guide):
        e = Excursion([], fake_excursion_guide, datetime(2025, 6, 1), 60)
        assert e.count_points() == 0


class TestExcursionRoute:
    def test_add_point_success(self, excursion):
        from museum_core.Hall import Hall
        h = Hall(99, 100.0)
        assert excursion.add_route_point(h) is True
        assert h in excursion.route_points

    def test_add_point_none_raises(self, excursion):
        with pytest.raises(ValueError):
            excursion.add_route_point(None)

    def test_add_point_duplicate_raises(self, excursion, sample_hall):
        with pytest.raises(ValueError):
            excursion.add_route_point(sample_hall)

    def test_add_point_after_start_raises(self, excursion):
        from museum_core.Hall import Hall
        excursion.start()
        with pytest.raises(InvalidExhibitStateException):
            excursion.add_route_point(Hall(99, 100.0))

    def test_remove_point_success(self, excursion, sample_hall):
        assert excursion.remove_route_point(sample_hall) is True
        assert sample_hall not in excursion.route_points

    def test_remove_point_none_raises(self, excursion):
        with pytest.raises(ValueError):
            excursion.remove_route_point(None)

    def test_remove_point_not_present_raises(self, excursion):
        from museum_core.Hall import Hall
        with pytest.raises(ValueError):
            excursion.remove_route_point(Hall(99, 100.0))

    def test_remove_point_after_start_raises(self, excursion, sample_hall):
        excursion.start()
        with pytest.raises(InvalidExhibitStateException):
            excursion.remove_route_point(sample_hall)

    def test_optimize_route_sorts_by_number(self, fake_excursion_guide):
        from museum_core.Hall import Hall
        h3 = Hall(3, 100.0)
        h1 = Hall(1, 100.0)
        h2 = Hall(2, 100.0)
        e = Excursion([h3, h1, h2], fake_excursion_guide,
                      datetime(2025, 6, 1), 60)
        e.optimize_route()
        assert [h.number for h in e.route_points] == [1, 2, 3]

    def test_optimize_route_after_start_raises(self, excursion):
        excursion.start()
        with pytest.raises(InvalidExhibitStateException):
            excursion.optimize_route()


class TestExcursionVisitors:
    def test_add_success(self, excursion, visitor):
        assert excursion.add_visitor(visitor) is True
        assert visitor in excursion.visitors

    def test_add_none_raises(self, excursion):
        with pytest.raises(ValueError):
            excursion.add_visitor(None)

    def test_add_duplicate_raises(self, excursion, visitor):
        excursion.add_visitor(visitor)
        with pytest.raises(ValueError):
            excursion.add_visitor(visitor)

    def test_add_after_finish_raises(self, excursion, visitor):
        excursion.start()
        excursion.finish()
        from museum_people.Visitor import Visitor
        with pytest.raises(InvalidExhibitStateException):
            excursion.add_visitor(Visitor("Other", 30))

    def test_count_visitors(self, excursion, visitor):
        excursion.add_visitor(visitor)
        assert excursion.count_visitors() == 1


class TestExcursionLifecycle:
    def test_start_success(self, excursion):
        assert excursion.start() is True
        assert excursion.is_started is True
        assert excursion.is_active is True

    def test_start_twice_raises(self, excursion):
        excursion.start()
        with pytest.raises(InvalidExhibitStateException):
            excursion.start()

    def test_start_empty_route_raises(self, fake_excursion_guide):
        e = Excursion([], fake_excursion_guide, datetime(2025, 6, 1), 60)
        with pytest.raises(InvalidExhibitStateException):
            e.start()

    def test_finish_success(self, excursion):
        excursion.start()
        assert excursion.finish() is True
        assert excursion.is_finished is True
        assert excursion.is_active is False


    def test_finish_twice_raises(self, excursion):
        excursion.start()
        excursion.finish()
        with pytest.raises(InvalidExhibitStateException):
            excursion.finish()


class TestExcursionChangeGuide:
    def test_change_success(self, excursion):
        from museum_people.Guide import Guide
        new_guide = Guide("New", 50000.0, date(2020, 1, 1), ["ru"], 3)
        assert excursion.change_guide(new_guide) is True
        assert excursion.guide is new_guide

    def test_change_none_raises(self, excursion):
        with pytest.raises(ValueError):
            excursion.change_guide(None)

    def test_change_after_start_raises(self, excursion):
        from museum_people.Guide import Guide
        excursion.start()
        new_guide = Guide("New", 50000.0, date(2020, 1, 1), ["ru"], 3)
        with pytest.raises(InvalidExhibitStateException):
            excursion.change_guide(new_guide)


class TestExcursionEncapsulation:
    def test_route_points_returns_copy(self, excursion):
        points = excursion.route_points
        points.append("fake")
        assert len(excursion.route_points) == 1

    def test_visitors_returns_copy(self, excursion, visitor):
        excursion.add_visitor(visitor)
        v = excursion.visitors
        v.append("fake")
        assert excursion.count_visitors() == 1