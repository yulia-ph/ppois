from exceptions.InvalidTicketException import InvalidTicketException
from museum_people.Employee import Employee
from museum_sales.Ticket import Ticket


class Cashier(Employee):
    """A museum cashier.

    Sells tickets, accepts payments, and handles refunds. Tracks the
    current shift's cash register total and the list of tickets sold
    during this shift.
    """

    def __init__(self, name: str, salary: float, hire_date, shift: str):
        """Initialize a cashier.

        Args:
            name: Employee name. Must not be empty.
            salary: Monthly salary. Must be non-negative.
            hire_date: Date of hire. Must not be None.
            shift: The shift label (e.g. "morning", "day"). Must not be empty.

        Raises:
            ValueError: If inherited validation fails, or shift is empty.
        """
        super().__init__(name, salary, hire_date)
        if not shift:
            raise ValueError("Shift must not be empty")
        self._shift = shift
        self._cash_in_register = 0.0
        self._sold_tickets = []


    @property
    def shift(self):
        return self._shift

    @property
    def cash_in_register(self):
        return self._cash_in_register

    @property
    def sold_tickets(self):
        return list(self._sold_tickets)


    def sell_ticket(self, ticket_type, visitor, date_) -> Ticket:
        """Sell a ticket to a visitor.

        Args:
            ticket_type: The ticket type. Must not be None.
            visitor: The visitor buying the ticket. Must not be None.
            date_: The date the ticket is valid for. Must not be None.

        Returns:
            The newly created and delivered Ticket.

        Raises:
            ValueError: If any argument is None.
            InvalidTicketException: If the visitor is not eligible for
                this ticket type.
        """
        if ticket_type is None:
            raise ValueError("Ticket type must not be None")
        if visitor is None:
            raise ValueError("Visitor must not be None")
        if date_ is None:
            raise ValueError("Ticket date must not be None")
        if not ticket_type.is_eligible(visitor):
            raise InvalidTicketException(
                reason=f"Visitor '{visitor.name}' is not eligible "
                       f"for ticket type '{ticket_type.name}'"
            )

        ticket = Ticket(ticket_type, date_)
        visitor.receive_ticket(ticket)
        self._sold_tickets.append(ticket)
        self._cash_in_register += ticket.cost
        return ticket

    def accept_payment(self, payment):
        """Accept a payment into the register.

        Args:
            payment: The payment to process. Must not be None.

        Returns:
            True on success.

        Raises:
            ValueError: If payment is None.
            InvalidExhibitStateException: Propagated if the payment is not
                pending.
        """
        if payment is None:
            raise ValueError("Payment must not be None")
        payment.process()
        self._cash_in_register += payment.amount
        return True


    def close_shift(self) -> float:
        """Close the shift and return the total cash in the register.

        Resets the register to 0.
        """
        result = self._cash_in_register
        self._cash_in_register = 0.0
        return result


    def refund_ticket(self, ticket) -> float:
        """Refund a ticket and return the refunded amount.

        Args:
            ticket: The ticket to refund. Must not be None.

        Returns:
            The refunded amount.

        Raises:
            ValueError: If ticket is None.
            InvalidTicketException: Propagated from ticket.refund() if
                the ticket cannot be refunded.
        """
        if ticket is None:
            raise ValueError("Ticket must not be None")
        amount = ticket.refund()
        self._cash_in_register -= amount
        return amount