from datetime import date

from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
from exceptions.InvalidTicketException import InvalidTicketException
from museum_sales.Ticket import Ticket
from museum_sales.TicketType import TicketType


class Visitor:
    """A museum visitor.

    A visitor may hold a ticket, a membership, and a museum card.
    The visitor tracks whether they are currently inside the museum
    and keeps a history of visit dates.

    A visitor enters the museum only with a valid ticket. Membership
    affects pricing (handled by TicketType and Order), and the card
    is a payment wallet (handled by MuseumCard).
    """

    def __init__(self, name: str, age: int):
        """Initialize a visitor.

        Args:
            name: The visitor's name. Must not be empty.
            age: The visitor's age. Must be non-negative.

        Raises:
            ValueError: If name is empty or age is negative.
        """
        if not name:
            raise ValueError("Visitor name must not be empty")
        if age < 0:
            raise ValueError(f"Age must be non-negative, got {age}")
        self._name = name
        self._age = age
        self._ticket = None
        self._membership = None
        self._card = None
        self._is_inside = False
        self._visit_history = []


    @property
    def name(self):
        return self._name

    @property
    def age(self):
        return self._age

    @property
    def ticket(self):
        return self._ticket

    @property
    def membership(self):
        return self._membership

    @property
    def card(self):
        return self._card

    @property
    def is_inside(self):
        return self._is_inside

    @property
    def visit_history(self):
        return list(self._visit_history)


    def buy_ticket(self, ticket_type: TicketType, date_: date) -> Ticket:
        """Buy a ticket of the given type.

        Args:
            ticket_type: The ticket type. The visitor must be eligible
                for it.
            date_: The date the ticket is valid for.

        Returns:
            The newly created Ticket.

        Raises:
            InvalidTicketException: If the visitor is not eligible for
                this ticket type.
        """
        if not ticket_type.is_eligible(self):
            raise InvalidTicketException(
                reason=f"Visitor '{self._name}' is not eligible "
                       f"for ticket type '{ticket_type.name}'"
            )
        ticket = Ticket(ticket_type, date_)
        self._ticket = ticket
        return ticket

    def receive_ticket(self, ticket: Ticket):
        """Receive a ticket (e.g. bought at the cashier).

        Args:
            ticket: The ticket to receive. Must not be None.

        Raises:
            ValueError: If ticket is None.
        """
        if ticket is None:
            raise ValueError("Ticket must not be None")
        self._ticket = ticket
        return True


    def get_membership(self, membership):
        """Attach a membership to this visitor.

        Args:
            membership: The membership. Must not be None.

        Raises:
            ValueError: If membership is None.
        """
        if membership is None:
            raise ValueError("Membership must not be None")
        self._membership = membership
        return True

    def get_card(self, card):
        """Attach a museum card to this visitor.

        Args:
            card: The card. Must not be None.

        Raises:
            ValueError: If card is None.
        """
        if card is None:
            raise ValueError("Card must not be None")
        self._card = card
        return True


    def enter_museum(self):
        """Enter the museum.

        Requires a valid ticket.

        Raises:
            InvalidExhibitStateException: If the visitor is already
                inside, or has no ticket.
            InvalidTicketException: Propagated from Ticket.validate()
                when the ticket is not valid today.
        """
        if self._is_inside:
            raise InvalidExhibitStateException(
                exhibit_title=self._name,
                state="inside",
                reason="Visitor is already inside the museum",
            )
        if self._ticket is None:
            raise InvalidExhibitStateException(
                exhibit_title=self._name,
                state="no_ticket",
                reason="Cannot enter the museum without a ticket",
            )
        self._ticket.validate()
        self._is_inside = True
        self._visit_history.append(date.today())
        return True

    def leave_museum(self):
        """Leave the museum.

        Idempotent: calling when the visitor is not inside is not an
        error.
        """
        self._is_inside = False
        return True

    def is_regular(self) -> bool:
        """Return True if the visitor has visited more than 5 times."""
        return len(self._visit_history) > 5