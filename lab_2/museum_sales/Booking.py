from exceptions.InvalidExhibitStateException import InvalidExhibitStateException


class Booking:
    """A pre-booking of tickets for a specific date.

    A booking collects tickets for one date and moves through statuses:

        PENDING -> CONFIRMED -> PAID
                    |
                    v
                CANCELLED

    Tickets can only be added or removed while the booking is PENDING.
    Payment is only allowed after CONFIRMED. Cancelling a paid booking
    refunds the payment by default.
    """

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_PAID = "paid"
    STATUS_CANCELLED = "cancelled"

    def __init__(self, visitor, date_):
        """Initialize a booking.

        Args:
            visitor: The visitor placing the booking. Must not be None.
            date_: The date the tickets are valid for. Must not be None.

        Raises:
            ValueError: If visitor or date_ is None.
        """
        if visitor is None:
            raise ValueError("Visitor must not be None")
        if date_ is None:
            raise ValueError("Date must not be None")
        self._visitor = visitor
        self._date = date_
        self._tickets = []
        self._payments = []
        self._status = Booking.STATUS_PENDING


    @property
    def visitor(self):
        return self._visitor

    @property
    def date(self):
        return self._date

    @property
    def tickets(self):
        return list(self._tickets)

    @property
    def payments(self):
        return list(self._payments)

    @property
    def status(self):
        return self._status

    @property
    def is_paid(self):
        return self._status == Booking.STATUS_PAID

    @property
    def is_cancelled(self):
        return self._status == Booking.STATUS_CANCELLED

    @property
    def is_pending(self):
        return self._status == Booking.STATUS_PENDING

    @property
    def is_confirmed(self):
        return self._status == Booking.STATUS_CONFIRMED


    def add_ticket(self, ticket):
        """Add a ticket to the booking.

        The ticket's date must match the booking's date.

        Args:
            ticket: The ticket to add. Must not be None.

        Raises:
            ValueError: If ticket is None, its date does not match the
                booking date, or the ticket is already in the booking.
        """
        if ticket is None:
            raise ValueError("Ticket must not be None")
        if ticket.date != self._date:
            raise ValueError(
                f"Ticket date {ticket.date} does not match "
                f"booking date {self._date}"
            )
        if ticket in self._tickets:
            raise ValueError(
                f"Ticket '{ticket.number}' is already in the booking"
            )
        self._tickets.append(ticket)
        return True

    def remove_ticket(self, ticket):
        """Remove a ticket from the booking.

        Only allowed while the booking is PENDING.

        Args:
            ticket: The ticket to remove. Must not be None.

        Raises:
            ValueError: If ticket is None or not in the booking.
            InvalidExhibitStateException: If the booking is not pending.
        """
        if ticket is None:
            raise ValueError("Ticket must not be None")
        if self._status != Booking.STATUS_PENDING:
            raise InvalidExhibitStateException(
                exhibit_title=f"Booking for {self._visitor.name}",
                state=self._status,
                reason="Cannot remove tickets from a non-pending booking",
            )
        if ticket not in self._tickets:
            raise ValueError(
                f"Ticket '{ticket.number}' is not in the booking"
            )
        self._tickets.remove(ticket)
        return True


    def calculate_total(self) -> float:
        """Return the total cost of all tickets in the booking."""
        return sum(t.cost for t in self._tickets)


    def confirm(self):
        """Confirm the booking, moving it from PENDING to CONFIRMED.

        Raises:
            InvalidExhibitStateException: If the booking is not pending.
            ValueError: If the booking has no tickets.
        """
        if self._status != Booking.STATUS_PENDING:
            raise InvalidExhibitStateException(
                exhibit_title=f"Booking for {self._visitor.name}",
                state=self._status,
                reason="Cannot confirm a booking that is not pending",
            )
        if not self._tickets:
            raise ValueError("Cannot confirm a booking with no tickets")
        self._status = Booking.STATUS_CONFIRMED
        return True

    def pay(self, payment):
        """Pay for the confirmed booking.

        Args:
            payment: The payment to use. Must expose `.amount` and
                `.process()`.

        Returns:
            True on success.

        Raises:
            InvalidExhibitStateException: If the booking is not confirmed.
            ValueError: If the payment amount does not match the total.
            PaymentFailedException: Propagated from payment.process().
        """
        if self._status != Booking.STATUS_CONFIRMED:
            raise InvalidExhibitStateException(
                exhibit_title=f"Booking for {self._visitor.name}",
                state=self._status,
                reason="Cannot pay a booking that is not confirmed",
            )
        total = self.calculate_total()
        if payment.amount != total:
            raise ValueError(
                f"Payment amount {payment.amount} does not match "
                f"booking total {total}"
            )
        payment.process()
        self._payments.append(payment)
        self._status = Booking.STATUS_PAID
        return True

    def cancel(self, refund: bool = True):
        """Cancel the booking.

        Args:
            refund: If True and the booking was paid, all payments are
                refunded.

        Idempotent: cancelling an already cancelled booking is not an
        error.
        """
        if self._status == Booking.STATUS_CANCELLED:
            return True

        if self._status == Booking.STATUS_PAID and refund:
            for payment in self._payments:
                payment.refund()

        self._status = Booking.STATUS_CANCELLED
        return True