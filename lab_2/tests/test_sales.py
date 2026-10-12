"""Tests for the museum_sales package.

Covers: Ticket, TicketType, Membership, MuseumCard, Payment,
ShopItem, Order, Booking. Sections are added as each class is
implemented.
"""
from datetime import date, timedelta

import pytest

from exceptions.InvalidTicketException import InvalidTicketException


class TestTicketTypeInit:
    def test_init_stores_fields(self, adult_ticket_type):
        assert adult_ticket_type.name == "Adult"
        assert adult_ticket_type.cost == 500.0
        assert adult_ticket_type.min_age == 18
        assert adult_ticket_type.max_age is None

    def test_init_with_max_age(self, child_ticket_type):
        assert child_ticket_type.min_age is None
        assert child_ticket_type.max_age == 17

    def test_init_with_both_bounds(self, student_ticket_type):
        assert student_ticket_type.min_age == 16
        assert student_ticket_type.max_age == 25

    def test_init_empty_name_raises(self):
        from museum_sales.TicketType import TicketType
        with pytest.raises(ValueError):
            TicketType("", 500.0)

    def test_init_negative_cost_raises(self):
        from museum_sales.TicketType import TicketType
        with pytest.raises(ValueError):
            TicketType("Adult", -1.0)

    def test_init_negative_min_age_raises(self):
        from museum_sales.TicketType import TicketType
        with pytest.raises(ValueError):
            TicketType("X", 100.0, min_age=-1)

    def test_init_negative_max_age_raises(self):
        from museum_sales.TicketType import TicketType
        with pytest.raises(ValueError):
            TicketType("X", 100.0, max_age=-1)

    def test_init_min_greater_than_max_raises(self):
        from museum_sales.TicketType import TicketType
        with pytest.raises(ValueError):
            TicketType("X", 100.0, min_age=30, max_age=18)


class TestTicketTypeIsEligible:
    def test_eligible_adult(self, adult_ticket_type):
        from museum_people.Visitor import Visitor
        v = Visitor("Anna", 25)
        assert adult_ticket_type.is_eligible(v) is True

    def test_not_eligible_adult_too_young(self, adult_ticket_type):
        from museum_people.Visitor import Visitor
        v = Visitor("Kid", 12)
        assert adult_ticket_type.is_eligible(v) is False

    def test_at_min_age_boundary(self, adult_ticket_type):
        from museum_people.Visitor import Visitor
        v = Visitor("Borderline", 18)
        assert adult_ticket_type.is_eligible(v) is True

    def test_child_eligible(self, child_ticket_type):
        from museum_people.Visitor import Visitor
        v = Visitor("Kid", 10)
        assert child_ticket_type.is_eligible(v) is True

    def test_child_not_eligible_adult(self, child_ticket_type):
        from museum_people.Visitor import Visitor
        v = Visitor("Anna", 25)
        assert child_ticket_type.is_eligible(v) is False

    def test_at_max_age_boundary(self, child_ticket_type):
        from museum_people.Visitor import Visitor
        v = Visitor("Teen", 17)
        assert child_ticket_type.is_eligible(v) is True

    def test_student_eligible_in_range(self, student_ticket_type):
        from museum_people.Visitor import Visitor
        v = Visitor("Student", 20)
        assert student_ticket_type.is_eligible(v) is True

    def test_student_not_eligible_too_young(self, student_ticket_type):
        from museum_people.Visitor import Visitor
        v = Visitor("Kid", 10)
        assert student_ticket_type.is_eligible(v) is False

    def test_student_not_eligible_too_old(self, student_ticket_type):
        from museum_people.Visitor import Visitor
        v = Visitor("Adult", 30)
        assert student_ticket_type.is_eligible(v) is False

    def test_no_bounds_always_eligible(self):
        from museum_people.Visitor import Visitor
        from museum_sales.TicketType import TicketType
        t = TicketType("Universal", 100.0)
        assert t.is_eligible(Visitor("Baby", 0)) is True
        assert t.is_eligible(Visitor("Ancient", 120)) is True


class TestTicketTypeCalculatePrice:
    def test_price_no_membership(self, adult_ticket_type):
        from museum_people.Visitor import Visitor
        v = Visitor("Anna", 25)
        assert adult_ticket_type.calculate_price(v) == 500.0

    def test_price_with_active_membership(self, adult_ticket_type, fake_membership):
        from museum_people.Visitor import Visitor
        v = Visitor("Anna", 25)
        v.get_membership(fake_membership)  # 20% discount
        assert adult_ticket_type.calculate_price(v) == 400.0

    def test_price_with_inactive_membership(self, adult_ticket_type):
        from museum_people.Visitor import Visitor
        from tests.conftest import FakeMembership
        v = Visitor("Anna", 25)
        v.get_membership(FakeMembership(active=False, discount=0.2))
        assert adult_ticket_type.calculate_price(v) == 500.0

    def test_price_not_eligible_raises(self, adult_ticket_type):
        from museum_people.Visitor import Visitor
        v = Visitor("Kid", 10)
        with pytest.raises(InvalidTicketException):
            adult_ticket_type.calculate_price(v)

    def test_price_rounds_membership_discount(self, adult_ticket_type):
        from museum_people.Visitor import Visitor
        from tests.conftest import FakeMembership
        v = Visitor("Anna", 25)
        v.get_membership(FakeMembership(active=True, discount=0.33))
        # 500 * 0.67 = 335.0 (with float tolerance)
        assert adult_ticket_type.calculate_price(v) == pytest.approx(335.0)



class TestTicketInit:
    def test_init_stores_fields(self, ticket, adult_ticket_type):
        assert ticket.type is adult_ticket_type
        assert ticket.date == date.today()
        assert ticket.base_cost == 500.0
        assert ticket.cost == 500.0
        assert ticket.discount == 0.0

    def test_init_not_used_not_refunded(self, ticket):
        assert ticket.is_used is False
        assert ticket.is_refunded is False

    def test_init_no_exhibition(self, ticket):
        assert ticket.exhibition is None

    def test_init_with_exhibition(self, adult_ticket_type):
        from museum_sales.Ticket import Ticket
        exhibition = object()
        t = Ticket(adult_ticket_type, date.today(), exhibition=exhibition)
        assert t.exhibition is exhibition

    def test_init_generates_unique_number(self, adult_ticket_type):
        from museum_sales.Ticket import Ticket
        t1 = Ticket(adult_ticket_type, date.today())
        t2 = Ticket(adult_ticket_type, date.today())
        assert t1.number != t2.number

    def test_init_number_format(self, ticket):
        assert ticket.number.startswith("T-")
        assert len(ticket.number) == 8

    def test_init_none_type_raises(self):
        from museum_sales.Ticket import Ticket
        with pytest.raises(ValueError):
            Ticket(None, date.today())

    def test_init_none_date_raises(self, adult_ticket_type):
        from museum_sales.Ticket import Ticket
        with pytest.raises(ValueError):
            Ticket(adult_ticket_type, None)


class TestTicketValidate:
    def test_validate_success(self, ticket):
        assert ticket.validate() is True

    def test_validate_used_raises(self, ticket_used):
        with pytest.raises(InvalidTicketException):
            ticket_used.validate()

    def test_validate_refunded_raises(self, ticket_refunded):
        with pytest.raises(InvalidTicketException):
            ticket_refunded.validate()

    def test_validate_yesterday_raises(self, ticket_yesterday):
        with pytest.raises(InvalidTicketException):
            ticket_yesterday.validate()

    def test_validate_tomorrow_raises(self, adult_ticket_type):
        from museum_sales.Ticket import Ticket
        t = Ticket(adult_ticket_type, date.today() + timedelta(days=1))
        with pytest.raises(InvalidTicketException):
            t.validate()


class TestTicketMarkUsed:
    def test_mark_used_success(self, ticket):
        result = ticket.mark_used()
        assert result is True
        assert ticket.is_used is True

    def test_mark_used_twice_raises(self, ticket_used):
        with pytest.raises(InvalidTicketException):
            ticket_used.mark_used()

    def test_mark_used_refunded_raises(self, ticket_refunded):
        with pytest.raises(InvalidTicketException):
            ticket_refunded.mark_used()


class TestTicketRefund:
    def test_refund_success_returns_cost(self, ticket):
        amount = ticket.refund()
        assert amount == 500.0
        assert ticket.is_refunded is True

    def test_refund_with_discount(self, ticket):
        ticket.apply_discount(0.5)
        amount = ticket.refund()
        assert amount == 250.0

    def test_refund_used_raises(self, ticket_used):
        with pytest.raises(InvalidTicketException):
            ticket_used.refund()

    def test_refund_twice_raises(self, ticket_refunded):
        with pytest.raises(InvalidTicketException):
            ticket_refunded.refund()


class TestTicketDiscount:
    def test_apply_discount_success(self, ticket):
        result = ticket.apply_discount(0.2)
        assert result is True
        assert ticket.discount == 0.2
        assert ticket.cost == 400.0

    def test_apply_discount_zero_allowed(self, ticket):
        ticket.apply_discount(0.0)
        assert ticket.cost == 500.0

    def test_apply_discount_negative_raises(self, ticket):
        with pytest.raises(ValueError):
            ticket.apply_discount(-0.1)

    def test_apply_discount_one_raises(self, ticket):
        with pytest.raises(ValueError):
            ticket.apply_discount(1.0)

    def test_apply_discount_above_one_raises(self, ticket):
        with pytest.raises(ValueError):
            ticket.apply_discount(1.5)

    def test_apply_discount_does_not_mutate_base_cost(self, ticket):
        ticket.apply_discount(0.2)
        assert ticket.base_cost == 500.0

    def test_apply_discount_twice_overrides(self, ticket):
        ticket.apply_discount(0.2)
        ticket.apply_discount(0.5)
        assert ticket.cost == 250.0


class TestTicketCoversExhibition:
    def test_general_ticket_covers_any_exhibition(self, ticket):
        exhibition = object()
        assert ticket.covers_exhibition(exhibition) is True

    def test_specific_ticket_covers_same_exhibition(self, adult_ticket_type):
        from museum_sales.Ticket import Ticket
        exhibition = object()
        t = Ticket(adult_ticket_type, date.today(), exhibition=exhibition)
        assert t.covers_exhibition(exhibition) is True

    def test_specific_ticket_does_not_cover_other(self, adult_ticket_type):
        from museum_sales.Ticket import Ticket
        exhibition_a = object()
        exhibition_b = object()
        t = Ticket(adult_ticket_type, date.today(), exhibition=exhibition_a)
        assert t.covers_exhibition(exhibition_b) is False


class TestShopItemInit:
    def test_init_stores_fields(self, magnet):
        assert magnet.name == "Museum Magnet"
        assert magnet.price == 200.0
        assert magnet.stock == 50

    def test_init_empty_name_raises(self):
        from museum_sales.ShopItem import ShopItem
        with pytest.raises(ValueError):
            ShopItem("", 100.0, 10)

    def test_init_negative_price_raises(self):
        from museum_sales.ShopItem import ShopItem
        with pytest.raises(ValueError):
            ShopItem("X", -1.0, 10)

    def test_init_negative_stock_raises(self):
        from museum_sales.ShopItem import ShopItem
        with pytest.raises(ValueError):
            ShopItem("X", 100.0, -1)


class TestShopItemIsAvailable:
    def test_available_default_qty(self, magnet):
        assert magnet.is_available() is True

    def test_available_large_qty(self, magnet):
        assert magnet.is_available(50) is True

    def test_not_available_too_large_qty(self, magnet):
        assert magnet.is_available(51) is False

    def test_not_available_when_empty(self, sold_out_item):
        assert sold_out_item.is_available() is False


class TestShopItemSell:
    def test_sell_success(self, magnet):
        result = magnet.sell(2)
        assert result is True
        assert magnet.stock == 48

    def test_sell_default_qty(self, magnet):
        magnet.sell()
        assert magnet.stock == 49

    def test_sell_all_stock(self, magnet):
        magnet.sell(50)
        assert magnet.stock == 0

    def test_sell_zero_raises(self, magnet):
        with pytest.raises(ValueError):
            magnet.sell(0)

    def test_sell_negative_raises(self, magnet):
        with pytest.raises(ValueError):
            magnet.sell(-1)

    def test_sell_too_many_raises(self, magnet):
        from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
        with pytest.raises(InvalidExhibitStateException):
            magnet.sell(51)

    def test_sell_too_many_does_not_change_stock(self, magnet):
        from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
        with pytest.raises(InvalidExhibitStateException):
            magnet.sell(51)
        assert magnet.stock == 50

    def test_sell_from_empty_raises(self, sold_out_item):
        from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
        with pytest.raises(InvalidExhibitStateException):
            sold_out_item.sell(1)


class TestShopItemReplenish:
    def test_replenish_success(self, magnet):
        result = magnet.replenish(10)
        assert result is True
        assert magnet.stock == 60

    def test_replenish_empty_item(self, sold_out_item):
        sold_out_item.replenish(5)
        assert sold_out_item.stock == 5

    def test_replenish_zero_raises(self, magnet):
        with pytest.raises(ValueError):
            magnet.replenish(0)

    def test_replenish_negative_raises(self, magnet):
        with pytest.raises(ValueError):
            magnet.replenish(-5)


class TestPaymentInit:
    def test_init_stores_fields(self, payment_card):
        assert payment_card.amount == 500.0
        assert payment_card.method == "card"

    def test_init_status_pending(self, payment_card):
        assert payment_card.status == "pending"
        assert payment_card.is_pending is True

    def test_init_not_paid(self, payment_card):
        assert payment_card.is_paid is False
        assert payment_card.is_refunded is False


    def test_init_zero_amount_raises(self):
        from museum_sales.Payment import Payment
        with pytest.raises(ValueError):
            Payment(0.0, Payment.METHOD_CASH)

    def test_init_negative_amount_raises(self):
        from museum_sales.Payment import Payment
        with pytest.raises(ValueError):
            Payment(-100.0, Payment.METHOD_CASH)

    def test_init_invalid_method_raises(self):
        from museum_sales.Payment import Payment
        with pytest.raises(ValueError):
            Payment(100.0, "crypto")


class TestPaymentProcess:
    def test_process_success(self, payment_card):
        result = payment_card.process()
        assert result is True
        assert payment_card.is_paid is True
        assert payment_card.status == "paid"

    def test_process_twice_raises(self, payment_paid):
        from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
        with pytest.raises(InvalidExhibitStateException):
            payment_paid.process()

    def test_process_refunded_raises(self, payment_refunded):
        from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
        with pytest.raises(InvalidExhibitStateException):
            payment_refunded.process()

    def test_process_cash_success(self, payment_cash):
        assert payment_cash.process() is True


class TestPaymentRefund:
    def test_refund_success(self, payment_paid):
        result = payment_paid.refund()
        assert result is True
        assert payment_paid.is_refunded is True
        assert payment_paid.is_paid is False

    def test_refund_pending_raises(self, payment_card):
        from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
        with pytest.raises(InvalidExhibitStateException):
            payment_card.refund()

    def test_refund_twice_raises(self, payment_refunded):
        from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
        with pytest.raises(InvalidExhibitStateException):
            payment_refunded.refund()


class TestOrderInit:
    def test_init_stores_buyer(self, order, visitor):
        assert order.buyer is visitor

    def test_init_empty_items(self, order):
        assert order.items == []

    def test_init_status_pending(self, order):
        assert order.status == "pending"
        assert order.is_paid is False
        assert order.is_cancelled is False

    def test_init_no_payment(self, order):
        assert order.payment is None

    def test_init_none_buyer_raises(self):
        from museum_sales.Order import Order
        with pytest.raises(ValueError):
            Order(None)


class TestOrderAddItem:
    def test_add_success(self, order, magnet):
        result = order.add_item(magnet, 1)
        assert result is True
        assert (magnet, 1) in order.items

    def test_add_default_qty(self, order, magnet):
        order.add_item(magnet)
        assert (magnet, 1) in order.items

    def test_add_same_item_accumulates_qty(self, order, magnet):
        order.add_item(magnet, 2)
        order.add_item(magnet, 3)
        assert (magnet, 5) in order.items
        assert len(order.items) == 1

    def test_add_none_raises(self, order):
        with pytest.raises(ValueError):
            order.add_item(None)

    def test_add_zero_qty_raises(self, order, magnet):
        with pytest.raises(ValueError):
            order.add_item(magnet, 0)

    def test_add_negative_qty_raises(self, order, magnet):
        with pytest.raises(ValueError):
            order.add_item(magnet, -1)

    def test_add_too_many_raises(self, order, magnet):
        from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
        with pytest.raises(InvalidExhibitStateException):
            order.add_item(magnet, 999)

    def test_add_empty_item_raises(self, order, sold_out_item):
        from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
        with pytest.raises(InvalidExhibitStateException):
            order.add_item(sold_out_item, 1)


class TestOrderRemoveItem:
    def test_remove_success(self, order_with_items, magnet):
        result = order_with_items.remove_item(magnet)
        assert result is True
        assert all(it is not magnet for it, _ in order_with_items.items)

    def test_remove_none_raises(self, order):
        with pytest.raises(ValueError):
            order.remove_item(None)

    def test_remove_not_in_order_raises(self, order, magnet):
        with pytest.raises(ValueError):
            order.remove_item(magnet)


class TestOrderCalculateTotal:
    def test_total_empty(self, order):
        assert order.calculate_total() == 0.0

    def test_total_single_item(self, order, magnet):
        order.add_item(magnet, 2)
        assert order.calculate_total() == 400.0

    def test_total_multiple_items(self, order_with_items, magnet, book):
        # magnet 200 * 1 + book 500 * 2 = 1200
        assert order_with_items.calculate_total() == 1200.0

    def test_total_with_membership_discount(self, order_with_membership):
        # magnet 200 * 0.8 = 160
        assert order_with_membership.calculate_total() == pytest.approx(160.0)


class TestOrderCheckout:
    def test_checkout_success(self, order_with_items):
        from museum_sales.Payment import Payment
        total = order_with_items.calculate_total()
        payment = Payment(total, Payment.METHOD_CARD)
        result = order_with_items.checkout(payment)
        assert result is True
        assert order_with_items.is_paid is True
        assert order_with_items.payment is payment

    def test_checkout_deducts_stock(self, order_with_items, magnet, book):
        from museum_sales.Payment import Payment
        total = order_with_items.calculate_total()
        order_with_items.checkout(Payment(total, Payment.METHOD_CARD))
        assert magnet.stock == 49
        assert book.stock == 8

    def test_checkout_empty_raises(self, order):
        from museum_sales.Payment import Payment
        with pytest.raises(ValueError):
            order.checkout(Payment(0.01, Payment.METHOD_CARD))

    def test_checkout_already_paid_raises(self, paid_order):
        from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
        from museum_sales.Payment import Payment
        with pytest.raises(InvalidExhibitStateException):
            paid_order.checkout(Payment(1.0, Payment.METHOD_CARD))

    def test_checkout_amount_mismatch_raises(self, order_with_items):
        from museum_sales.Payment import Payment
        with pytest.raises(ValueError):
            order_with_items.checkout(Payment(1.0, Payment.METHOD_CARD))

    def test_checkout_failed_payment_propagates(self, order_with_items):
        from exceptions.PaymentFailedException import PaymentFailedException
        from tests.conftest import FakePayment
        total = order_with_items.calculate_total()
        failing = FakePayment(amount=total, succeed=False)
        with pytest.raises(PaymentFailedException):
            order_with_items.checkout(failing)

    def test_checkout_failed_payment_does_not_deduct(self, order_with_items, magnet):
        from exceptions.PaymentFailedException import PaymentFailedException
        from tests.conftest import FakePayment
        total = order_with_items.calculate_total()
        failing = FakePayment(amount=total, succeed=False)
        with pytest.raises(PaymentFailedException):
            order_with_items.checkout(failing)
        assert magnet.stock == 50


class TestOrderCancel:
    def test_cancel_pending(self, order_with_items):
        result = order_with_items.cancel()
        assert result is True
        assert order_with_items.is_cancelled is True

    def test_cancel_pending_does_not_refund(self, order_with_items, magnet):
        order_with_items.cancel()
        # stock unchanged because nothing was deducted
        assert magnet.stock == 50

    def test_cancel_paid_refunds_payment(self, paid_order):
        paid_order.cancel()
        assert paid_order.is_cancelled is True
        assert paid_order.payment.is_refunded is True

    def test_cancel_paid_returns_stock(self, paid_order, magnet, book):
        paid_order.cancel()
        assert magnet.stock == 50
        assert book.stock == 10

    def test_cancel_idempotent(self, order_with_items):
        order_with_items.cancel()
        assert order_with_items.cancel() is True


class TestOrderEncapsulation:
    def test_items_returns_copy(self, order_with_items):
        items = order_with_items.items
        items.append("fake")
        assert len(order_with_items.items) == 2


class TestBookingInit:
    def test_init_stores_fields(self, booking, visitor):
        assert booking.visitor is visitor
        assert booking.date == date.today()

    def test_init_empty_tickets(self, booking):
        assert booking.tickets == []

    def test_init_empty_payments(self, booking):
        assert booking.payments == []

    def test_init_status_pending(self, booking):
        assert booking.status == "pending"
        assert booking.is_pending is True

    def test_init_none_visitor_raises(self):
        from museum_sales.Booking import Booking
        with pytest.raises(ValueError):
            Booking(None, date.today())

    def test_init_none_date_raises(self, visitor):
        from museum_sales.Booking import Booking
        with pytest.raises(ValueError):
            Booking(visitor, None)


class TestBookingAddTicket:
    def test_add_success(self, booking, adult_ticket_type):
        from museum_sales.Ticket import Ticket
        t = Ticket(adult_ticket_type, date.today())
        result = booking.add_ticket(t)
        assert result is True
        assert t in booking.tickets

    def test_add_none_raises(self, booking):
        with pytest.raises(ValueError):
            booking.add_ticket(None)

    def test_add_wrong_date_raises(self, booking, adult_ticket_type):
        from museum_sales.Ticket import Ticket
        t = Ticket(adult_ticket_type, date.today() + timedelta(days=1))
        with pytest.raises(ValueError):
            booking.add_ticket(t)

    def test_add_duplicate_raises(self, booking, adult_ticket_type):
        from museum_sales.Ticket import Ticket
        t = Ticket(adult_ticket_type, date.today())
        booking.add_ticket(t)
        with pytest.raises(ValueError):
            booking.add_ticket(t)


class TestBookingRemoveTicket:
    def test_remove_success(self, booking_with_tickets):
        t = booking_with_tickets.tickets[0]
        result = booking_with_tickets.remove_ticket(t)
        assert result is True
        assert t not in booking_with_tickets.tickets

    def test_remove_none_raises(self, booking_with_tickets):
        with pytest.raises(ValueError):
            booking_with_tickets.remove_ticket(None)

    def test_remove_not_in_booking_raises(self, booking, adult_ticket_type):
        from museum_sales.Ticket import Ticket
        t = Ticket(adult_ticket_type, date.today())
        with pytest.raises(ValueError):
            booking.remove_ticket(t)

    def test_remove_after_confirm_raises(self, confirmed_booking):
        from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
        t = confirmed_booking.tickets[0]
        with pytest.raises(InvalidExhibitStateException):
            confirmed_booking.remove_ticket(t)


class TestBookingCalculateTotal:
    def test_total_empty(self, booking):
        assert booking.calculate_total() == 0.0

    def test_total_two_tickets(self, booking_with_tickets):
        # 2 * 500 = 1000
        assert booking_with_tickets.calculate_total() == 1000.0


class TestBookingConfirm:
    def test_confirm_success(self, booking_with_tickets):
        result = booking_with_tickets.confirm()
        assert result is True
        assert booking_with_tickets.is_confirmed is True

    def test_confirm_empty_raises(self, booking):
        with pytest.raises(ValueError):
            booking.confirm()

    def test_confirm_twice_raises(self, confirmed_booking):
        from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
        with pytest.raises(InvalidExhibitStateException):
            confirmed_booking.confirm()


class TestBookingPay:
    def test_pay_success(self, confirmed_booking):
        from museum_sales.Payment import Payment
        total = confirmed_booking.calculate_total()
        payment = Payment(total, Payment.METHOD_CARD)
        result = confirmed_booking.pay(payment)
        assert result is True
        assert confirmed_booking.is_paid is True
        assert payment in confirmed_booking.payments

    def test_pay_pending_raises(self, booking_with_tickets):
        from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
        from museum_sales.Payment import Payment
        with pytest.raises(InvalidExhibitStateException):
            booking_with_tickets.pay(Payment(1000.0, Payment.METHOD_CARD))

    def test_pay_amount_mismatch_raises(self, confirmed_booking):
        from museum_sales.Payment import Payment
        with pytest.raises(ValueError):
            confirmed_booking.pay(Payment(1.0, Payment.METHOD_CARD))

    def test_pay_failed_payment_propagates(self, confirmed_booking):
        from exceptions.PaymentFailedException import PaymentFailedException
        from tests.conftest import FakePayment
        total = confirmed_booking.calculate_total()
        failing = FakePayment(amount=total, succeed=False)
        with pytest.raises(PaymentFailedException):
            confirmed_booking.pay(failing)


class TestBookingCancel:
    def test_cancel_pending(self, booking_with_tickets):
        result = booking_with_tickets.cancel()
        assert result is True
        assert booking_with_tickets.is_cancelled is True

    def test_cancel_paid_refunds(self, paid_booking):
        payment = paid_booking.payments[0]
        paid_booking.cancel()
        assert payment.is_refunded is True

    def test_cancel_paid_without_refund(self, paid_booking):
        payment = paid_booking.payments[0]
        paid_booking.cancel(refund=False)
        assert payment.is_refunded is False

    def test_cancel_idempotent(self, booking_with_tickets):
        booking_with_tickets.cancel()
        assert booking_with_tickets.cancel() is True


class TestBookingEncapsulation:
    def test_tickets_returns_copy(self, booking_with_tickets):
        tickets = booking_with_tickets.tickets
        tickets.append("fake")
        assert len(booking_with_tickets.tickets) == 2

    def test_payments_returns_copy(self, paid_booking):
        payments = paid_booking.payments
        payments.append("fake")
        assert len(paid_booking.payments) == 1


class TestMembershipInit:
    def test_init_stores_fields(self, membership_silver, visitor):
        assert membership_silver.visitor is visitor
        assert membership_silver.level == "silver"

    def test_init_valid_until(self, membership_silver):
        assert membership_silver.valid_until == date.today() + timedelta(days=365)


    def test_init_none_visitor_raises(self):
        from museum_sales.Membership import Membership
        with pytest.raises(ValueError):
            Membership(None, "basic", date.today())

    def test_init_none_date_raises(self, visitor):
        from museum_sales.Membership import Membership
        with pytest.raises(ValueError):
            Membership(visitor, "basic", None)

    def test_init_invalid_level_raises(self, visitor):
        from museum_sales.Membership import Membership
        with pytest.raises(ValueError):
            Membership(visitor, "platinum", date.today())


class TestMembershipActive:
    def test_active_when_future(self, membership_silver):
        assert membership_silver.is_active() is True

    def test_active_on_valid_until_day(self, visitor):
        from museum_sales.Membership import Membership
        m = Membership(visitor, "basic", date.today())
        assert m.is_active() is True

    def test_not_active_when_expired(self, membership_expired):
        assert membership_expired.is_active() is False

    def test_check_discount_active(self, membership_silver):
        assert membership_silver.check_discount() == 0.20

    def test_check_discount_basic(self, membership_basic):
        assert membership_basic.check_discount() == 0.10

    def test_check_discount_gold(self, membership_gold):
        assert membership_gold.check_discount() == 0.50

    def test_check_discount_expired_returns_zero(self, membership_expired):
        assert membership_expired.check_discount() == 0.0


class TestMembershipRenew:
    def test_renew_active_extends_from_current(self, membership_silver):
        old_end = membership_silver.valid_until
        membership_silver.renew(6)
        assert membership_silver.valid_until == old_end + timedelta(days=180)

    def test_renew_expired_extends_from_today(self, membership_expired):
        membership_expired.renew(1)
        assert membership_expired.valid_until == date.today() + timedelta(days=30)


    def test_renew_negative_raises(self, membership_silver):
        with pytest.raises(ValueError):
            membership_silver.renew(-1)


class TestMuseumCardInit:
    def test_init_stores_fields(self, card, visitor):
        assert card.visitor is visitor
        assert card.balance == 1000.0

    def test_init_not_blocked(self, card):
        assert card.is_blocked is False

    def test_init_default_balance_zero(self, visitor):
        from museum_sales.MuseumCard import MuseumCard
        c = MuseumCard(visitor)
        assert c.balance == 0.0

    def test_init_none_visitor_raises(self):
        from museum_sales.MuseumCard import MuseumCard
        with pytest.raises(ValueError):
            MuseumCard(None)

    def test_init_negative_balance_raises(self, visitor):
        from museum_sales.MuseumCard import MuseumCard
        with pytest.raises(ValueError):
            MuseumCard(visitor, balance=-1.0)


class TestMuseumCardTopUp:
    def test_top_up_success(self, card):
        result = card.top_up(500.0)
        assert result is True
        assert card.balance == 1500.0

    def test_top_up_zero_raises(self, card):
        with pytest.raises(ValueError):
            card.top_up(0.0)

    def test_top_up_negative_raises(self, card):
        with pytest.raises(ValueError):
            card.top_up(-100.0)

    def test_top_up_blocked_raises(self, blocked_card):
        from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
        with pytest.raises(InvalidExhibitStateException):
            blocked_card.top_up(100.0)

    def test_top_up_blocked_does_not_change_balance(self, blocked_card):
        from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
        old = blocked_card.balance
        with pytest.raises(InvalidExhibitStateException):
            blocked_card.top_up(100.0)
        assert blocked_card.balance == old


class TestMuseumCardPay:
    def test_pay_success(self, card):
        result = card.pay(300.0)
        assert result is True
        assert card.balance == 700.0

    def test_pay_exact_balance(self, card):
        card.pay(1000.0)
        assert card.balance == 0.0

    def test_pay_zero_raises(self, card):
        with pytest.raises(ValueError):
            card.pay(0.0)

    def test_pay_negative_raises(self, card):
        with pytest.raises(ValueError):
            card.pay(-10.0)

    def test_pay_blocked_raises(self, blocked_card):
        from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
        with pytest.raises(InvalidExhibitStateException):
            blocked_card.pay(100.0)

    def test_pay_insufficient_funds_raises(self, empty_card):
        from exceptions.InsufficientFundsException import InsufficientFundsException
        with pytest.raises(InsufficientFundsException):
            empty_card.pay(100.0)

    def test_pay_insufficient_does_not_change_balance(self, card):
        from exceptions.InsufficientFundsException import InsufficientFundsException
        with pytest.raises(InsufficientFundsException):
            card.pay(2000.0)
        assert card.balance == 1000.0

    def test_pay_insufficient_reports_shortfall(self, card):
        from exceptions.InsufficientFundsException import InsufficientFundsException
        try:
            card.pay(1500.0)
        except InsufficientFundsException as e:
            assert e.required == 1500.0
            assert e.available == 1000.0
            assert e.shortfall == 500.0


class TestMuseumCardBlock:
    def test_block_success(self, card):
        result = card.block()
        assert result is True
        assert card.is_blocked is True

    def test_block_idempotent(self, card):
        card.block()
        assert card.block() is True
        assert card.is_blocked is True

    def test_unblock_success(self, blocked_card):
        result = blocked_card.unblock()
        assert result is True
        assert blocked_card.is_blocked is False

    def test_unblock_idempotent(self, card):
        assert card.unblock() is True
        assert card.is_blocked is False

    def test_unblock_allows_operations(self, blocked_card):
        blocked_card.unblock()
        assert blocked_card.top_up(100.0) is True
        assert blocked_card.pay(50.0) is True