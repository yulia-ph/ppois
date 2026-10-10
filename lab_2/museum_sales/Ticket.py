from datetime import date

from exceptions.InvalidTicketException import InvalidTicketException


class Ticket:
    """A museum entry ticket.

    A ticket is valid for a single day and can be used once. Its price
    is fixed at the moment of purchase. A ticket can optionally be
    tied to a specific exhibition.
    """

    _counter = 0

    def __init__(self, type_, date_, exhibition=None):
        """Initialize a ticket.

        Args:
            type_: The ticket type (TicketType). Must expose `.cost`.
            date_: The date the ticket is valid for.
            exhibition: Optional exhibition this ticket grants access to.
                If None, the ticket is a general admission ticket.

        Raises:
            ValueError: If type_ or date_ is None.
        """
        if type_ is None:
            raise ValueError("Ticket type must not be None")
        if date_ is None:
            raise ValueError("Ticket date must not be None")

        Ticket._counter += 1
        self._number = f"T-{Ticket._counter:06d}"
        self._type = type_
        self._date = date_
        self._exhibition = exhibition
        self._base_cost = type_.cost
        self._discount = 0.0
        self._is_used = False
        self._is_refunded = False


    @property
    def number(self):
        return self._number

    @property
    def cost(self):
        return self._base_cost * (1 - self._discount)

    @property
    def base_cost(self):
        return self._base_cost

    @property
    def discount(self):
        return self._discount

    @property
    def type(self):
        return self._type

    @property
    def date(self):
        return self._date

    @property
    def exhibition(self):
        return self._exhibition

    @property
    def is_used(self):
        return self._is_used

    @property
    def is_refunded(self):
        return self._is_refunded


    def validate(self):
        """Check that the ticket can be used today.

        Raises:
            InvalidTicketException: If the ticket is already used,
                refunded, or not valid for today's date.

        Returns:
            True if valid.
        """
        if self._is_used:
            raise InvalidTicketException(
                ticket_number=self._number,
                reason="Ticket has already been used",
            )
        if self._is_refunded:
            raise InvalidTicketException(
                ticket_number=self._number,
                reason="Ticket has been refunded",
            )
        if self._date != date.today():
            raise InvalidTicketException(
                ticket_number=self._number,
                reason=f"Ticket is valid for {self._date}, not for today",
            )
        return True


    def mark_used(self):
        """Mark the ticket as used.

        Raises:
            InvalidTicketException: If the ticket is already used or
                refunded.
        """
        if self._is_used:
            raise InvalidTicketException(
                ticket_number=self._number,
                reason="Ticket has already been used",
            )
        if self._is_refunded:
            raise InvalidTicketException(
                ticket_number=self._number,
                reason="Ticket has been refunded",
            )
        self._is_used = True
        return True

    def refund(self):
        """Refund the ticket.

        Raises:
            InvalidTicketException: If the ticket was already used or
                already refunded.

        Returns:
            The refund amount.
        """
        if self._is_used:
            raise InvalidTicketException(
                ticket_number=self._number,
                reason="Cannot refund a used ticket",
            )
        if self._is_refunded:
            raise InvalidTicketException(
                ticket_number=self._number,
                reason="Ticket has already been refunded",
            )
        self._is_refunded = True
        return self.cost


    def apply_discount(self, discount: float):
        """Apply a discount rate to the ticket.

        Args:
            discount: Discount as a fraction in [0, 1).

        Raises:
            ValueError: If discount is outside [0, 1).
        """
        if discount < 0 or discount >= 1:
            raise ValueError(f"Discount must be in [0, 1), got {discount}")
        self._discount = discount
        return True


    def covers_exhibition(self, exhibition) -> bool:
        """Return True if this ticket grants access to the exhibition.

        General admission tickets (no exhibition set) cover all
        exhibitions.
        """
        if self._exhibition is None:
            return True
        return self._exhibition is exhibition