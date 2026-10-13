"""Tests for the museum_people package.

Covers: Employee, Visitor, Curator, Restorer, Guide, Cashier,
Administrator, SecurityGuard. Sections are added as each class is
implemented.
"""
from datetime import date, timedelta

import pytest

from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
from exceptions.InvalidTicketException import InvalidTicketException
from tests.conftest import FakePayment


class TestEmployeeInit:
    def test_init_stores_fields(self, employee):
        assert employee.name == "Ivanov"
        assert employee.salary == 50000.0
        assert employee.hire_date == date(2020, 1, 1)

    def test_init_not_on_vacation(self, employee):
        assert employee.on_vacation is False
        assert employee.vacations == []

    def test_init_position_is_class_name(self, employee):
        assert employee.position == "Employee"

    def test_init_empty_name_raises(self):
        from museum_people.Employee import Employee
        with pytest.raises(ValueError):
            Employee("", 50000.0, date(2020, 1, 1))

    def test_init_negative_salary_raises(self):
        from museum_people.Employee import Employee
        with pytest.raises(ValueError):
            Employee("A", -1.0, date(2020, 1, 1))

    def test_init_none_hire_date_raises(self):
        from museum_people.Employee import Employee
        with pytest.raises(ValueError):
            Employee("A", 50000.0, None)


class TestEmployeeWork:
    def test_work_when_not_on_vacation(self, employee):
        assert employee.work() is True

    def test_work_when_on_vacation(self, employee_on_vacation):
        assert employee_on_vacation.work() is False


class TestEmployeeSalary:

    def test_raise_salary_success(self, employee):
        result = employee.raise_salary(60000.0)
        assert result is True
        assert employee.salary == 60000.0

    def test_raise_to_same_amount_allowed(self, employee):
        assert employee.raise_salary(50000.0) is True
        assert employee.salary == 50000.0

    def test_raise_zero_raises(self, employee):
        with pytest.raises(ValueError):
            employee.raise_salary(0.0)

    def test_raise_negative_raises(self, employee):
        with pytest.raises(ValueError):
            employee.raise_salary(-100.0)

    def test_raise_lower_raises(self, employee):
        with pytest.raises(ValueError):
            employee.raise_salary(40000.0)


class TestEmployeeVacation:
    def test_take_vacation_success(self, employee):
        result = employee.take_vacation(date(2024, 6, 1), 14)
        assert result is True
        assert employee.on_vacation is True
        assert len(employee.vacations) == 1

    def test_take_vacation_zero_days_raises(self, employee):
        with pytest.raises(ValueError):
            employee.take_vacation(date(2024, 6, 1), 0)

    def test_take_vacation_negative_days_raises(self, employee):
        with pytest.raises(ValueError):
            employee.take_vacation(date(2024, 6, 1), -5)

    def test_take_vacation_none_start_raises(self, employee):
        with pytest.raises(ValueError):
            employee.take_vacation(None, 14)

    def test_take_vacation_when_already_on_vacation_raises(self, employee_on_vacation):
        with pytest.raises(InvalidExhibitStateException):
            employee_on_vacation.take_vacation(date(2024, 9, 1), 7)

    def test_return_from_vacation_success(self, employee_on_vacation):
        result = employee_on_vacation.return_from_vacation()
        assert result is True
        assert employee_on_vacation.on_vacation is False

    def test_return_from_vacation_idempotent(self, employee):
        """Returning when not on vacation is not an error."""
        assert employee.return_from_vacation() is True
        assert employee.on_vacation is False


class TestVisitorInit:
    def test_init_stores_fields(self, visitor):
        assert visitor.name == "Anna"
        assert visitor.age == 25

    def test_init_no_ticket(self, visitor):
        assert visitor.ticket is None

    def test_init_no_membership(self, visitor):
        assert visitor.membership is None

    def test_init_no_card(self, visitor):
        assert visitor.card is None

    def test_init_not_inside(self, visitor):
        assert visitor.is_inside is False

    def test_init_visit_history_empty(self, visitor):
        assert visitor.visit_history == []
        assert len(visitor.visit_history) == 0

    def test_init_empty_name_raises(self):
        from museum_people.Visitor import Visitor
        with pytest.raises(ValueError):
            Visitor("", 25)

    def test_init_negative_age_raises(self):
        from museum_people.Visitor import Visitor
        with pytest.raises(ValueError):
            Visitor("Anna", -1)


class TestVisitorBuyTicket:
    def test_buy_success(self, visitor, fake_visitor_ticket_type):
        ticket = visitor.buy_ticket(fake_visitor_ticket_type, date.today())
        assert ticket is not None
        assert visitor.ticket is ticket

    def test_buy_returns_ticket_with_correct_type(self, visitor, fake_visitor_ticket_type):
        ticket = visitor.buy_ticket(fake_visitor_ticket_type, date.today())
        assert ticket.type is fake_visitor_ticket_type
        assert ticket.cost == 500.0

    def test_buy_ineligible_raises(self, visitor, fake_visitor_ticket_type_ineligible):
        with pytest.raises(InvalidTicketException):
            visitor.buy_ticket(fake_visitor_ticket_type_ineligible, date.today())

    def test_buy_ineligible_does_not_attach_ticket(self, visitor, fake_visitor_ticket_type_ineligible):
        with pytest.raises(InvalidTicketException):
            visitor.buy_ticket(fake_visitor_ticket_type_ineligible, date.today())
        assert visitor.ticket is None


class TestVisitorReceiveTicket:
    def test_receive_success(self, visitor, fake_visitor_ticket_type):
        from museum_sales.Ticket import Ticket
        ticket = Ticket(fake_visitor_ticket_type, date.today())
        assert visitor.receive_ticket(ticket) is True
        assert visitor.ticket is ticket

    def test_receive_none_raises(self, visitor):
        with pytest.raises(ValueError):
            visitor.receive_ticket(None)

    def test_receive_overwrites_previous(self, visitor, fake_visitor_ticket_type):
        from museum_sales.Ticket import Ticket
        t1 = Ticket(fake_visitor_ticket_type, date.today())
        t2 = Ticket(fake_visitor_ticket_type, date.today())
        visitor.receive_ticket(t1)
        visitor.receive_ticket(t2)
        assert visitor.ticket is t2


class TestVisitorMembershipAndCard:
    def test_get_membership_success(self, visitor, fake_membership):
        assert visitor.get_membership(fake_membership) is True
        assert visitor.membership is fake_membership

    def test_get_membership_none_raises(self, visitor):
        with pytest.raises(ValueError):
            visitor.get_membership(None)

    def test_get_card_success(self, visitor, fake_card):
        assert visitor.get_card(fake_card) is True
        assert visitor.card is fake_card


class TestVisitorEnterMuseum:
    def test_enter_success(self, visitor_with_ticket):
        result = visitor_with_ticket.enter_museum()
        assert result is True
        assert visitor_with_ticket.is_inside is True

    def test_enter_records_visit(self, visitor_with_ticket):
        visitor_with_ticket.enter_museum()
        assert len(visitor_with_ticket.visit_history) == 1
        assert visitor_with_ticket.visit_history[-1] == date.today()

    def test_enter_no_ticket_raises(self, visitor):
        with pytest.raises(InvalidExhibitStateException):
            visitor.enter_museum()

    def test_enter_already_inside_raises(self, visitor_with_ticket):
        visitor_with_ticket.enter_museum()
        with pytest.raises(InvalidExhibitStateException):
            visitor_with_ticket.enter_museum()

    def test_enter_with_invalid_ticket_raises(self, visitor, fake_visitor_ticket_type):
        """A ticket for yesterday is not valid today."""
        from museum_sales.Ticket import Ticket
        yesterday = date.today() - timedelta(days=1)
        ticket = Ticket(fake_visitor_ticket_type, yesterday)
        visitor.receive_ticket(ticket)
        with pytest.raises(InvalidTicketException):
            visitor.enter_museum()

    def test_enter_with_used_ticket_raises(self, visitor, fake_visitor_ticket_type):
        """Marking the ticket used then entering should fail."""
        from museum_sales.Ticket import Ticket
        ticket = Ticket(fake_visitor_ticket_type, date.today())
        ticket.mark_used()
        visitor.receive_ticket(ticket)
        with pytest.raises(InvalidTicketException):
            visitor.enter_museum()


class TestVisitorLeaveMuseum:
    def test_leave_success(self, visitor_with_ticket):
        visitor_with_ticket.enter_museum()
        result = visitor_with_ticket.leave_museum()
        assert result is True
        assert visitor_with_ticket.is_inside is False

    def test_leave_idempotent(self, visitor):
        """Leaving when not inside is not an error."""
        assert visitor.leave_museum() is True
        assert visitor.is_inside is False


class TestVisitorRegular:
    def test_not_regular_by_default(self, visitor):
        assert visitor.is_regular() is False

    def test_not_regular_at_5_visits(self, visitor):
        visitor._visit_history = [date.today()] * 5
        assert visitor.is_regular() is False

    def test_regular_at_6_visits(self, visitor):
        visitor._visit_history = [date.today()] * 6
        assert visitor.is_regular() is True


class TestVisitorEncapsulation:
    def test_visit_history_property_returns_copy(self, visitor_with_ticket):
        visitor_with_ticket.enter_museum()
        hist = visitor_with_ticket.visit_history
        hist.append("fake")
        assert len(visitor_with_ticket.visit_history) == 1


class TestAdministratorInit:
    def test_init_stores_fields(self, administrator):
        assert administrator.name == "Sidorov"
        assert administrator.department == "management"

    def test_init_empty_department_raises(self):
        from museum_people.Administrator import Administrator
        with pytest.raises(ValueError):
            Administrator("A", 50000.0, date(2020, 1, 1), "")

    def test_init_inherits_employee_validation(self):
        from museum_people.Administrator import Administrator
        with pytest.raises(ValueError):
            Administrator("", 50000.0, date(2020, 1, 1), "management")


class TestAdministratorApproveLoan:
    def test_approve_success(self, administrator, fake_loan):
        result = administrator.approve_loan(fake_loan)
        assert result is True
        assert fake_loan.is_approved is True

    def test_approve_none_raises(self, administrator):
        with pytest.raises(ValueError):
            administrator.approve_loan(None)

    def test_approve_overdue_raises(self, administrator, fake_loan_overdue):
        from exceptions.LoanOverdueException import LoanOverdueException
        with pytest.raises(LoanOverdueException):
            administrator.approve_loan(fake_loan_overdue)


class TestAdministratorPayInvoice:


    def test_pay_success(self, administrator, fake_invoice, fake_payment_ok):
        result = administrator.pay_invoice(fake_invoice, fake_payment_ok)
        assert result is True
        assert fake_invoice.is_paid is True
        assert fake_invoice in administrator.invoices

    def test_pay_none_invoice_raises(self, administrator, fake_payment_ok):
        with pytest.raises(ValueError):
            administrator.pay_invoice(None, fake_payment_ok)

    def test_pay_none_payment_raises(self, administrator, fake_invoice):
        with pytest.raises(ValueError):
            administrator.pay_invoice(fake_invoice, None)

    def test_pay_amount_mismatch_raises(self, administrator, fake_invoice):
        wrong = FakePayment(amount=999.0)
        with pytest.raises(ValueError):
            administrator.pay_invoice(fake_invoice, wrong)

    def test_pay_process_fails_raises(self, administrator, fake_invoice, fake_payment_fail):
        from exceptions.PaymentFailedException import PaymentFailedException
        with pytest.raises(PaymentFailedException):
            administrator.pay_invoice(fake_invoice, fake_payment_fail)

    def test_pay_already_paid_invoice_raises(self, administrator, fake_invoice_paid, fake_payment_ok):
        from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
        with pytest.raises(InvalidExhibitStateException):
            administrator.pay_invoice(fake_invoice_paid, fake_payment_ok)


class TestAdministratorHire:
    def test_hire_success(self, administrator, fake_museum):
        from museum_people.Employee import Employee
        e = Employee("Novikov", 40000.0, date(2024, 1, 1))
        result = administrator.hire_employee(fake_museum, e)
        assert result is True
        assert e in fake_museum.employees
        assert e in administrator.hired_employees

    def test_hire_none_museum_raises(self, administrator):
        from museum_people.Employee import Employee
        e = Employee("A", 40000.0, date(2024, 1, 1))
        with pytest.raises(ValueError):
            administrator.hire_employee(None, e)

    def test_hire_none_employee_raises(self, administrator, fake_museum):
        with pytest.raises(ValueError):
            administrator.hire_employee(fake_museum, None)

    def test_hire_duplicate_raises(self, administrator, fake_museum):
        from museum_people.Employee import Employee
        e = Employee("Novikov", 40000.0, date(2024, 1, 1))
        administrator.hire_employee(fake_museum, e)
        with pytest.raises(ValueError):
            administrator.hire_employee(fake_museum, e)


class TestAdministratorFire:
    def test_fire_success(self, administrator, fake_museum):
        from museum_people.Employee import Employee
        e = Employee("Novikov", 40000.0, date(2024, 1, 1))
        administrator.hire_employee(fake_museum, e)
        result = administrator.fire_employee(fake_museum, e)
        assert result is True
        assert e not in fake_museum.employees

    def test_fire_none_museum_raises(self, administrator):
        from museum_people.Employee import Employee
        e = Employee("A", 40000.0, date(2024, 1, 1))
        with pytest.raises(ValueError):
            administrator.fire_employee(None, e)

    def test_fire_none_employee_raises(self, administrator, fake_museum):
        with pytest.raises(ValueError):
            administrator.fire_employee(fake_museum, None)

    def test_fire_not_in_museum_raises(self, administrator, fake_museum):
        from museum_people.Employee import Employee
        e = Employee("A", 40000.0, date(2024, 1, 1))
        with pytest.raises(ValueError):
            administrator.fire_employee(fake_museum, e)


class TestCashierInit:
    def test_init_stores_fields(self, cashier):
        assert cashier.name == "Petrova"
        assert cashier.shift == "day"

    def test_init_register_zero(self, cashier):
        assert cashier.cash_in_register == 0.0

    def test_init_no_sold_tickets(self, cashier):
        assert cashier.sold_tickets == []

    def test_init_position_is_class_name(self, cashier):
        assert cashier.position == "Cashier"

    def test_init_empty_shift_raises(self):
        from museum_people.Cashier import Cashier
        with pytest.raises(ValueError):
            Cashier("A", 50000.0, date(2020, 1, 1), "")


class TestCashierSellTicket:
    def test_sell_success(self, cashier, cashier_visitor, fake_visitor_ticket_type):
        ticket = cashier.sell_ticket(fake_visitor_ticket_type, cashier_visitor, date.today())
        assert ticket is not None
        assert cashier_visitor.ticket is ticket
        assert ticket in cashier.sold_tickets
        assert cashier.cash_in_register == 500.0

    def test_sell_none_type_raises(self, cashier, cashier_visitor):
        with pytest.raises(ValueError):
            cashier.sell_ticket(None, cashier_visitor, date.today())

    def test_sell_none_visitor_raises(self, cashier, fake_visitor_ticket_type):
        with pytest.raises(ValueError):
            cashier.sell_ticket(fake_visitor_ticket_type, None, date.today())

    def test_sell_none_date_raises(self, cashier, cashier_visitor, fake_visitor_ticket_type):
        with pytest.raises(ValueError):
            cashier.sell_ticket(fake_visitor_ticket_type, cashier_visitor, None)

    def test_sell_ineligible_raises(self, cashier, cashier_visitor, fake_visitor_ticket_type_ineligible):
        from exceptions.InvalidTicketException import InvalidTicketException
        with pytest.raises(InvalidTicketException):
            cashier.sell_ticket(
                fake_visitor_ticket_type_ineligible,
                cashier_visitor,
                date.today(),
            )

    def test_sell_ineligible_does_not_change_register(self, cashier, cashier_visitor, fake_visitor_ticket_type_ineligible):
        from exceptions.InvalidTicketException import InvalidTicketException
        with pytest.raises(InvalidTicketException):
            cashier.sell_ticket(
                fake_visitor_ticket_type_ineligible,
                cashier_visitor,
                date.today(),
            )
        assert cashier.cash_in_register == 0.0

    def test_sell_multiple_accumulates(self, cashier, cashier_visitor, fake_visitor_ticket_type):
        cashier.sell_ticket(fake_visitor_ticket_type, cashier_visitor, date.today())
        cashier.sell_ticket(fake_visitor_ticket_type, cashier_visitor, date.today())
        assert cashier.cash_in_register == 1000.0
        assert len(cashier.sold_tickets) == 2


class TestCashierAcceptPayment:
    def test_accept_success(self, cashier, fake_payment_ok):
        result = cashier.accept_payment(fake_payment_ok)
        assert result is True
        assert cashier.cash_in_register == 1000.0

    def test_accept_none_raises(self, cashier):
        with pytest.raises(ValueError):
            cashier.accept_payment(None)

    def test_accept_failed_payment_raises(self, cashier, fake_payment_fail):
        from exceptions.PaymentFailedException import PaymentFailedException
        with pytest.raises(PaymentFailedException):
            cashier.accept_payment(fake_payment_fail)

    def test_accept_failed_payment_no_register_change(self, cashier, fake_payment_fail):
        from exceptions.PaymentFailedException import PaymentFailedException
        with pytest.raises(PaymentFailedException):
            cashier.accept_payment(fake_payment_fail)
        assert cashier.cash_in_register == 0.0


class TestCashierCloseShift:
    def test_close_returns_total(self, cashier, fake_payment_ok):
        cashier.accept_payment(fake_payment_ok)
        result = cashier.close_shift()
        assert result == 1000.0

    def test_close_resets_register(self, cashier, fake_payment_ok):
        cashier.accept_payment(fake_payment_ok)
        cashier.close_shift()
        assert cashier.cash_in_register == 0.0

    def test_close_empty_returns_zero(self, cashier):
        assert cashier.close_shift() == 0.0


class TestCashierRefundTicket:
    def test_refund_success(self, cashier, cashier_visitor, fake_visitor_ticket_type):
        ticket = cashier.sell_ticket(
            fake_visitor_ticket_type, cashier_visitor, date.today()
        )
        register_before = cashier.cash_in_register
        amount = cashier.refund_ticket(ticket)
        assert amount == 500.0
        assert cashier.cash_in_register == register_before - 500.0

    def test_refund_none_raises(self, cashier):
        with pytest.raises(ValueError):
            cashier.refund_ticket(None)

    def test_refund_used_ticket_raises(self, cashier, cashier_visitor, fake_visitor_ticket_type):
        from exceptions.InvalidTicketException import InvalidTicketException
        ticket = cashier.sell_ticket(
            fake_visitor_ticket_type, cashier_visitor, date.today()
        )
        ticket.mark_used()
        with pytest.raises(InvalidTicketException):
            cashier.refund_ticket(ticket)

    def test_refund_twice_raises(self, cashier, cashier_visitor, fake_visitor_ticket_type):
        from exceptions.InvalidTicketException import InvalidTicketException
        ticket = cashier.sell_ticket(
            fake_visitor_ticket_type, cashier_visitor, date.today()
        )
        cashier.refund_ticket(ticket)
        with pytest.raises(InvalidTicketException):
            cashier.refund_ticket(ticket)


class TestGuideInit:
    def test_init_stores_fields(self, guide):
        assert guide.name == "Smirnova"
        assert guide.experience_years == 5
        assert "ru" in guide.languages
        assert "en" in guide.languages

    def test_init_tours_empty(self, guide):
        assert guide.tours == []

    def test_init_position_is_class_name(self, guide):
        assert guide.position == "Guide"

    def test_init_empty_languages_raises(self):
        from museum_people.Guide import Guide
        with pytest.raises(ValueError):
            Guide("A", 45000.0, date(2020, 1, 1), [], 5)

    def test_init_negative_experience_raises(self):
        from museum_people.Guide import Guide
        with pytest.raises(ValueError):
            Guide("A", 45000.0, date(2020, 1, 1), ["en"], -1)


class TestGuideLanguages:
    def test_speak_language_true(self, guide):
        assert guide.speak_language("ru") is True

    def test_speak_language_false(self, guide):
        assert guide.speak_language("de") is False


class TestGuideConductTour:
    def test_conduct_success(self, guide, fake_excursion):
        result = guide.conduct_tour(fake_excursion)
        assert result is True
        assert fake_excursion in guide.tours
        assert fake_excursion.is_started is True

    def test_conduct_none_raises(self, guide):
        with pytest.raises(ValueError):
            guide.conduct_tour(None)

    def test_conduct_cannot_start_raises(self, guide, fake_excursion_cannot_start):
        from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
        with pytest.raises(InvalidExhibitStateException):
            guide.conduct_tour(fake_excursion_cannot_start)

    def test_conduct_cannot_start_does_not_append(self, guide, fake_excursion_cannot_start):
        from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
        with pytest.raises(InvalidExhibitStateException):
            guide.conduct_tour(fake_excursion_cannot_start)
        assert fake_excursion_cannot_start not in guide.tours


class TestGuideFinishTour:
    def test_finish_success(self, guide, fake_excursion):
        guide.conduct_tour(fake_excursion)
        result = guide.finish_tour(fake_excursion)
        assert result is True
        assert fake_excursion.is_finished is True

    def test_finish_none_raises(self, guide):
        with pytest.raises(ValueError):
            guide.finish_tour(None)


class TestGuideEncapsulation:
    def test_languages_returns_copy(self, guide):
        langs = guide.languages
        langs.append("xx")
        assert "xx" not in guide.languages

    def test_tours_returns_copy(self, guide, fake_excursion):
        guide.conduct_tour(fake_excursion)
        tours = guide.tours
        tours.append("fake")
        assert len(guide.tours) == 1


class TestCuratorInit:
    def test_init_stores_fields(self, curator):
        assert curator.name == "Sokolova"
        assert curator.specialization == "painting"

    def test_init_empty_collections(self, curator):
        assert curator.collections == []

    def test_init_empty_exhibitions(self, curator):
        assert curator.exhibitions == []

    def test_init_position_is_class_name(self, curator):
        assert curator.position == "Curator"

    def test_init_empty_specialization_raises(self):
        from museum_people.Curator import Curator
        with pytest.raises(ValueError):
            Curator("A", 70000.0, date(2020, 1, 1), "")


class TestCuratorCurateCollection:
    def test_curate_success(self, curator, collection):
        result = curator.curate_collection(collection)
        assert result is True
        assert collection in curator.collections

    def test_curate_none_raises(self, curator):
        with pytest.raises(ValueError):
            curator.curate_collection(None)

    def test_curate_duplicate_raises(self, curator, collection):
        curator.curate_collection(collection)
        with pytest.raises(ValueError):
            curator.curate_collection(collection)


class TestCuratorCreateExhibition:
    def test_create_success(self, curator, monkeypatch):
        from museum_exhibitions import Exhibition as exhibition_module

        class FakeExhibition:
            def __init__(self, title, start, end, curator_, type_):
                self.title = title
                self.start_date = start
                self.end_date = end
                self.curator = curator_
                self.type = type_

        monkeypatch.setattr(exhibition_module, "Exhibition", FakeExhibition)
        exhibition = curator.create_exhibition(
            "Impressionists", date(2024, 1, 1), date(2024, 12, 31)
        )
        assert exhibition.title == "Impressionists"
        assert exhibition.curator is curator
        assert exhibition in curator.exhibitions

    def test_create_empty_title_raises(self, curator):
        with pytest.raises(ValueError):
            curator.create_exhibition("", date(2024, 1, 1), date(2024, 12, 31))

    def test_create_none_start_raises(self, curator):
        with pytest.raises(ValueError):
            curator.create_exhibition("X", None, date(2024, 12, 31))

    def test_create_none_end_raises(self, curator):
        with pytest.raises(ValueError):
            curator.create_exhibition("X", date(2024, 1, 1), None)

    def test_create_end_before_start_raises(self, curator):
        with pytest.raises(ValueError):
            curator.create_exhibition("X", date(2024, 12, 31), date(2024, 1, 1))

    def test_create_end_equals_start_raises(self, curator):
        d = date(2024, 6, 1)
        with pytest.raises(ValueError):
            curator.create_exhibition("X", d, d)

    def test_create_invalid_type_raises(self, curator):
        with pytest.raises(ValueError):
            curator.create_exhibition(
                "X", date(2024, 1, 1), date(2024, 12, 31),
                exhibition_type="unknown",
            )


class TestCuratorSelectExhibits:
    def test_select_from_empty_collection(self, curator, collection):
        assert curator.select_exhibits(collection) == []

    def test_select_only_available(self, curator, collection_with_exhibits):
        # collection_with_exhibits has 3 exhibits, one with available=False
        result = curator.select_exhibits(collection_with_exhibits, count=10)
        assert len(result) == 2
        assert all(e.is_available_for_exhibition() for e in result)

    def test_select_limits_by_count(self, curator, collection_with_exhibits):
        result = curator.select_exhibits(collection_with_exhibits, count=1)
        assert len(result) == 1

    def test_select_none_collection_raises(self, curator):
        with pytest.raises(ValueError):
            curator.select_exhibits(None)

    def test_select_zero_count_raises(self, curator, collection):
        with pytest.raises(ValueError):
            curator.select_exhibits(collection, count=0)


class TestCuratorApproveLoan:
    def test_approve_success(self, curator, fake_loan_pending):
        result = curator.approve_loan(fake_loan_pending)
        assert result is True
        assert fake_loan_pending.is_approved is True

    def test_approve_none_raises(self, curator):
        with pytest.raises(ValueError):
            curator.approve_loan(None)

    def test_approve_overdue_raises(self, curator, fake_loan_overdue):
        from exceptions.LoanOverdueException import LoanOverdueException
        with pytest.raises(LoanOverdueException):
            curator.approve_loan(fake_loan_overdue)

    def test_approve_failing_loan_raises(self, curator, fake_loan_that_fails):
        from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
        with pytest.raises(InvalidExhibitStateException):
            curator.approve_loan(fake_loan_that_fails)


class TestCuratorEncapsulation:
    def test_collections_returns_copy(self, curator, collection):
        curator.curate_collection(collection)
        colls = curator.collections
        colls.append("fake")
        assert len(curator.collections) == 1


class TestRestorerInit:
    def test_init_stores_fields(self, restorer):
        assert restorer.name == "Ivanov"
        assert restorer.specialization == "painting"
        assert restorer.certificate == "cert-123"

    def test_init_tasks_empty(self, restorer):
        assert restorer.tasks == []

    def test_init_position_is_class_name(self, restorer):
        assert restorer.position == "Restorer"

    def test_init_empty_specialization_raises(self):
        from museum_people.Restorer import Restorer
        with pytest.raises(ValueError):
            Restorer("A", 60000.0, date(2020, 1, 1), "", "cert")

    def test_init_empty_certificate_raises(self):
        from museum_people.Restorer import Restorer
        with pytest.raises(ValueError):
            Restorer("A", 60000.0, date(2020, 1, 1), "painting", "")


class TestRestorerRestoreExhibit:
    def test_restore_success(self, restorer, exhibit_damaged, restoration_module_stub):
        result = restorer.restore_exhibit(exhibit_damaged)
        assert result is not None
        assert result.exhibit is exhibit_damaged
        assert result.restorer is restorer
        assert result.is_started is True
        assert result in restorer.tasks

    def test_restore_critical_allowed(self, restorer, exhibit_critical, restoration_module_stub):
        """Critical exhibits need restoration the most — must be allowed."""
        result = restorer.restore_exhibit(exhibit_critical)
        assert result is not None

    def test_restore_none_raises(self, restorer):
        with pytest.raises(ValueError):
            restorer.restore_exhibit(None)

    def test_restore_healthy_exhibit_raises(self, restorer, exhibit):
        from exceptions.RestorationException import RestorationException
        with pytest.raises(RestorationException):
            restorer.restore_exhibit(exhibit)

    def test_restore_excellent_raises(self, restorer):
        from exceptions.RestorationException import RestorationException
        from museum_exhibits.Exhibit import Exhibit
        e = Exhibit("T", "A", condition="excellent")
        with pytest.raises(RestorationException):
            restorer.restore_exhibit(e)

    def test_restore_does_not_append_on_failure(self, restorer, exhibit):
        from exceptions.RestorationException import RestorationException
        with pytest.raises(RestorationException):
            restorer.restore_exhibit(exhibit)
        assert restorer.tasks == []


class TestRestorerMakeReport:
    def test_make_report_success(self, restorer, exhibit_damaged, restoration_module_stub):
        restoration = restorer.restore_exhibit(exhibit_damaged)
        restoration.complete_restoration()
        report = restorer.make_restoration_report(restoration)
        assert report is not None

    def test_make_report_incomplete_raises(self, restorer, exhibit_damaged, restoration_module_stub):
        from exceptions.RestorationException import RestorationException
        restoration = restorer.restore_exhibit(exhibit_damaged)
        # not completed yet
        with pytest.raises(RestorationException):
            restorer.make_restoration_report(restoration)

    def test_make_report_none_raises(self, restorer):
        with pytest.raises(ValueError):
            restorer.make_restoration_report(None)


class TestRestorerEstimateCost:
    def test_estimate_good(self, restorer, exhibit):
        assert restorer.estimate_cost(exhibit) == 1000.0

    def test_estimate_damaged(self, restorer, exhibit_damaged):
        assert restorer.estimate_cost(exhibit_damaged) == 2000.0

    def test_estimate_critical(self, restorer, exhibit_critical):
        assert restorer.estimate_cost(exhibit_critical) == 5000.0

    def test_estimate_none_raises(self, restorer):
        with pytest.raises(ValueError):
            restorer.estimate_cost(None)


class TestRestorerEncapsulation:
    def test_tasks_returns_copy(self, restorer, exhibit_damaged, restoration_module_stub):
        restorer.restore_exhibit(exhibit_damaged)
        tasks = restorer.tasks
        tasks.append("fake")
        assert len(restorer.tasks) == 1


class TestSecurityGuardInit:
    def test_init_stores_fields(self, guard):
        assert guard.name == "Sidorov"
        assert guard.shift == "night"
        assert guard.zone == "hall-1"

    def test_init_journal_empty(self, guard):
        assert guard.journal == []

    def test_init_incidents_empty(self, guard):
        assert guard.incidents == []

    def test_init_position_is_class_name(self, guard):
        assert guard.position == "SecurityGuard"

    def test_init_empty_shift_raises(self):
        from museum_people.SecurityGuard import SecurityGuard
        with pytest.raises(ValueError):
            SecurityGuard("A", 40000.0, date(2020, 1, 1), "", "hall")

    def test_init_empty_zone_raises(self):
        from museum_people.SecurityGuard import SecurityGuard
        with pytest.raises(ValueError):
            SecurityGuard("A", 40000.0, date(2020, 1, 1), "day", "")


class TestSecurityGuardPatrol:
    def test_patrol_returns_zone(self, guard):
        assert guard.zone == "hall-1"


class TestSecurityGuardCheckAccess:
    def test_check_access_granted(self, guard, visitor_with_ticket, access_control_stub):
        result = guard.check_access(visitor_with_ticket, "public")
        assert result is True
        assert len(guard.journal) == 1

    def test_check_access_denied(self, guard, visitor, access_control_stub):
        # visitor has no ticket -> access denied
        result = guard.check_access(visitor, "public")
        assert result is False
        assert len(guard.journal) == 1

    def test_check_access_none_person_raises(self, guard):
        with pytest.raises(ValueError):
            guard.check_access(None, "public")

    def test_check_access_empty_zone_raises(self, guard, visitor_with_ticket):
        with pytest.raises(ValueError):
            guard.check_access(visitor_with_ticket, "")


class TestSecurityGuardReportIncident:
    def test_report_success(self, guard, incident_stub):
        incident = guard.report_incident("theft", "hall-1", "high")
        assert incident is not None
        assert incident.type == "theft"
        assert incident.place == "hall-1"
        assert incident.severity == "high"
        assert incident.guard is guard
        assert incident in guard.incidents

    def test_report_default_severity(self, guard, incident_stub):
        incident = guard.report_incident("theft", "hall-1")
        assert incident.severity == "medium"

    def test_report_empty_type_raises(self, guard):
        with pytest.raises(ValueError):
            guard.report_incident("", "hall-1")

    def test_report_empty_place_raises(self, guard):
        with pytest.raises(ValueError):
            guard.report_incident("theft", "")

    def test_report_invalid_severity_raises(self, guard):
        with pytest.raises(ValueError):
            guard.report_incident("theft", "hall-1", "catastrophic")

    def test_report_all_valid_severities(self, guard, incident_stub):
        for sev in ("low", "medium", "high"):
            incident = guard.report_incident("other", "hall-1", sev)
            assert incident.severity == sev


class TestSecurityGuardCloseIncident:
    def test_close_success(self, guard, incident_stub):
        incident = guard.report_incident("theft", "hall-1")
        result = guard.close_incident(incident)
        assert result is True
        assert incident.is_closed is True

    def test_close_none_raises(self, guard):
        with pytest.raises(ValueError):
            guard.close_incident(None)

    def test_close_twice_raises(self, guard, incident_stub):
        from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
        incident = guard.report_incident("theft", "hall-1")
        guard.close_incident(incident)
        with pytest.raises(InvalidExhibitStateException):
            guard.close_incident(incident)


class TestSecurityGuardOpenIncidents:
    def test_open_incidents_empty(self, guard):
        assert guard.get_open_incidents() == []

    def test_open_incidents_after_report(self, guard, incident_stub):
        guard.report_incident("theft", "hall-1")
        guard.report_incident("vandalism", "hall-2")
        assert len(guard.get_open_incidents()) == 2

    def test_open_incidents_excludes_closed(self, guard, incident_stub):
        i1 = guard.report_incident("theft", "hall-1")
        guard.report_incident("vandalism", "hall-2")
        guard.close_incident(i1)
        open_ones = guard.get_open_incidents()
        assert len(open_ones) == 1
        assert i1 not in open_ones


class TestSecurityGuardEncapsulation:
    def test_journal_returns_copy(self, guard, visitor_with_ticket, access_control_stub):
        guard.check_access(visitor_with_ticket, "public")
        journal = guard.journal
        journal.append("fake")
        assert len(guard.journal) == 1

    def test_incidents_returns_copy(self, guard, incident_stub):
        guard.report_incident("theft", "hall-1")
        incidents = guard.incidents
        incidents.append("fake")
        assert len(guard.incidents) == 1