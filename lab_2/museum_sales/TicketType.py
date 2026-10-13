from exceptions.InvalidTicketException import InvalidTicketException


class TicketType:
    """A ticket type (tariff) offered by the museum.

    Ticket types define pricing rules and eligibility constraints.
    Examples: "Adult" (min_age=18), "Child" (max_age=17), "Student"
    (min_age=16). The base cost is fixed, but a visitor with an active
    membership gets a discount.

    A ticket type does not know which visitors bought tickets — it
    only knows the tariff rules. Visitor eligibility is checked by
    Visitor.buy_ticket and Cashier.sell_ticket.
    """

    def __init__(self, name: str, cost: float,
                 min_age: int = None, max_age: int = None):
        """Initialize a ticket type.

        Args:
            name: The ticket type name. Must not be empty.
            cost: Base cost in conventional units. Must be non-negative.
            min_age: Optional minimum visitor age (inclusive).
            max_age: Optional maximum visitor age (inclusive).

        Raises:
            ValueError: If name is empty, cost is negative, or the age
                bounds are inconsistent.
        """
        if not name:
            raise ValueError("Ticket type name must not be empty")
        if cost < 0:
            raise ValueError(f"Cost must be non-negative, got {cost}")
        if min_age is not None and min_age < 0:
            raise ValueError(f"min_age must be non-negative, got {min_age}")
        if max_age is not None and max_age < 0:
            raise ValueError(f"max_age must be non-negative, got {max_age}")
        if (min_age is not None and max_age is not None
                and min_age > max_age):
            raise ValueError(
                f"min_age ({min_age}) must not exceed max_age ({max_age})"
            )

        self._name = name
        self._cost = cost
        self._min_age = min_age
        self._max_age = max_age


    @property
    def name(self):
        return self._name

    @property
    def cost(self):
        return self._cost

    @property
    def min_age(self):
        return self._min_age

    @property
    def max_age(self):
        return self._max_age


    def is_eligible(self, visitor) -> bool:
        """Return True if the visitor's age fits this ticket type.

        Args:
            visitor: The visitor to check. Must expose `.age`.
        """
        if self._min_age is not None and visitor.age < self._min_age:
            return False
        return not (self._max_age is not None and visitor.age > self._max_age)


    def calculate_price(self, visitor) -> float:
        """Calculate the price this visitor would pay.

        Applies the visitor's active membership discount if any.

        Args:
            visitor: The visitor. Must expose `.age` and optionally
                `.membership` (which may be None).

        Returns:
            The final price.

        Raises:
            InvalidTicketException: If the visitor is not eligible for
                this ticket type.
        """
        if not self.is_eligible(visitor):
            raise InvalidTicketException(
                reason=f"Visitor '{visitor.name}' is not eligible "
                       f"for ticket type '{self._name}'"
            )
        price = self._cost
        membership = getattr(visitor, "membership", None)
        if membership is not None and membership.is_active():
            price *= (1 - membership.check_discount())
        return price

    def __repr__(self):
        bounds = ""
        if self._min_age is not None:
            bounds += f" min={self._min_age}"
        if self._max_age is not None:
            bounds += f" max={self._max_age}"
        return f"<TicketType {self._name}: {self._cost}{bounds}>"