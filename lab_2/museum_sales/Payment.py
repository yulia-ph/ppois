from exceptions.InvalidExhibitStateException import InvalidExhibitStateException


class Payment:
    """A payment transaction.

    Represents the transfer of a sum of money via a chosen method
    (cash, card, online). A payment has a lifecycle:

        PENDING -> PAID -> REFUNDED
                  |
                  v
                FAILED

    The payment does not interact with external payment systems — it
    only tracks its own state. Callers are responsible for calling
    `process()` when the payment should be attempted and `refund()`
    when the money should be returned.
    """

    METHOD_CASH = "cash"
    METHOD_CARD = "card"
    METHOD_ONLINE = "online"

    VALID_METHODS = (METHOD_CASH, METHOD_CARD, METHOD_ONLINE)

    STATUS_PENDING = "pending"
    STATUS_PAID = "paid"
    STATUS_FAILED = "failed"
    STATUS_REFUNDED = "refunded"

    def __init__(self, amount: float, method: str):
        """Initialize a payment.

        Args:
            amount: Payment amount. Must be positive.
            method: Payment method. Must be one of the VALID_METHODS
                constants.

        Raises:
            ValueError: If amount is not positive, or method is not
                valid.
        """
        if amount <= 0:
            raise ValueError(f"Payment amount must be positive, got {amount}")
        if method not in Payment.VALID_METHODS:
            raise ValueError(
                f"Invalid payment method '{method}'. "
                f"Must be one of {Payment.VALID_METHODS}"
            )
        self._amount = amount
        self._method = method
        self._status = Payment.STATUS_PENDING

    @property
    def amount(self):
        return self._amount

    @property
    def method(self):
        return self._method

    @property
    def status(self):
        return self._status

    @property
    def is_paid(self):
        return self._status == Payment.STATUS_PAID

    @property
    def is_refunded(self):
        return self._status == Payment.STATUS_REFUNDED

    @property
    def is_pending(self):
        return self._status == Payment.STATUS_PENDING


    def process(self):
        """Process the payment: transition from PENDING to PAID.

        Raises:
            InvalidExhibitStateException: If the payment is not PENDING.
        """
        if self._status != Payment.STATUS_PENDING:
            raise InvalidExhibitStateException(
                exhibit_title=f"Payment {self._amount}",
                state=self._status,
                reason="Cannot process a payment that is not pending",
            )
        self._status = Payment.STATUS_PAID
        return True

    def refund(self):
        """Refund the payment: transition from PAID to REFUNDED.

        Raises:
            InvalidExhibitStateException: If the payment is not PAID.
        """
        if self._status != Payment.STATUS_PAID:
            raise InvalidExhibitStateException(
                exhibit_title=f"Payment {self._amount}",
                state=self._status,
                reason="Cannot refund a payment that is not paid",
            )
        self._status = Payment.STATUS_REFUNDED
        return True