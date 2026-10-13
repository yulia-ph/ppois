from exceptions.InsufficientFundsException import InsufficientFundsException
from exceptions.InvalidExhibitStateException import InvalidExhibitStateException


class MuseumCard:
    """A prepaid card used by a visitor to pay for museum services.

    A card stores a balance that can be topped up and spent on tickets,
    shop purchases, café orders, etc. A card can be blocked (e.g. if
    lost), in which case no top-ups or payments are allowed.

    The card is a wallet, not a membership: it holds money, not
    privileges. A visitor can have either, both, or neither.
    """

    def __init__(self, visitor, balance: float = 0.0):
        """Initialize a museum card.

        Args:
            visitor: The cardholder. Must not be None.
            balance: Initial balance. Must be non-negative.

        Raises:
            ValueError: If visitor is None or balance is negative.
        """
        if visitor is None:
            raise ValueError("Visitor must not be None")
        if balance < 0:
            raise ValueError(f"Balance must be non-negative, got {balance}")
        self._visitor = visitor
        self._balance = balance
        self._is_blocked = False


    @property
    def visitor(self):
        return self._visitor

    @property
    def balance(self):
        return self._balance

    @property
    def is_blocked(self):
        return self._is_blocked


    def top_up(self, amount: float):
        """Add funds to the card.

        Args:
            amount: Amount to add. Must be positive.

        Raises:
            ValueError: If amount is not positive.
            InvalidExhibitStateException: If the card is blocked.
        """
        if amount <= 0:
            raise ValueError(f"Top-up amount must be positive, got {amount}")
        if self._is_blocked:
            raise InvalidExhibitStateException(
                exhibit_title=f"Card for {self._visitor.name}",
                state="blocked",
                reason="Cannot top up a blocked card",
            )
        self._balance += amount
        return True


    def pay(self, amount: float):
        """Pay for a service using the card.

        Args:
            amount: Amount to deduct. Must be positive.

        Returns:
            True on success.

        Raises:
            ValueError: If amount is not positive.
            InvalidExhibitStateException: If the card is blocked.
            InsufficientFundsException: If the balance is too low.
        """
        if amount <= 0:
            raise ValueError(f"Payment amount must be positive, got {amount}")
        if self._is_blocked:
            raise InvalidExhibitStateException(
                exhibit_title=f"Card for {self._visitor.name}",
                state="blocked",
                reason="Cannot pay with a blocked card",
            )
        if self._balance < amount:
            raise InsufficientFundsException(
                required=amount,
                available=self._balance,
            )
        self._balance -= amount
        return True


    def block(self):
        """Block the card.

        Idempotent: blocking an already blocked card is not an error.
        """
        self._is_blocked = True
        return True

    def unblock(self):
        """Unblock the card.

        Idempotent: unblocking an already active card is not an error.
        """
        self._is_blocked = False
        return True