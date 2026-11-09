from exceptions.InvalidCargoStateException import InvalidCargoStateException
from exceptions.PaymentFailedException import PaymentFailedException


class Payment:
    """A payment. process() may run only once from PENDING."""

    METHOD_CASH = "cash"
    METHOD_CARD = "card"
    METHOD_TRANSFER = "transfer"

    VALID_METHODS = (METHOD_CASH, METHOD_CARD, METHOD_TRANSFER)

    STATUS_PENDING = "pending"
    STATUS_PAID = "paid"
    STATUS_FAILED = "failed"
    STATUS_REFUNDED = "refunded"

    def __init__(self, amount: float, method: str):
        if amount <= 0:
            raise ValueError(f"Payment amount must be positive, got {amount}")
        if method not in Payment.VALID_METHODS:
            raise ValueError(
                f"Invalid payment method '{method}'. Must be one of {Payment.VALID_METHODS}"
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
    def is_pending(self):
        return self._status == Payment.STATUS_PENDING

    def fail(self, reason: str = "declined"):
        """Mark the payment as failed and raise PaymentFailedException."""
        if self._status != Payment.STATUS_PENDING:
            raise InvalidCargoStateException(
                title=f"Payment {self._amount}",
                state=self._status,
                reason="Cannot fail a payment that is not pending",
            )
        self._status = Payment.STATUS_FAILED
        raise PaymentFailedException(amount=self._amount, method=self._method, reason=reason)

    def process(self):
        """PENDING -> PAID. A second call fails.

        Raises:
            PaymentFailedException: If the payment was already marked failed.
            InvalidCargoStateException: If the payment is not pending.
        """
        if self._status == Payment.STATUS_FAILED:
            raise PaymentFailedException(
                amount=self._amount,
                method=self._method,
                reason="Payment previously failed",
            )
        if self._status != Payment.STATUS_PENDING:
            raise InvalidCargoStateException(
                title=f"Payment {self._amount}",
                state=self._status,
                reason="Cannot process a payment that is not pending",
            )
        self._status = Payment.STATUS_PAID
        return True

    def refund(self):
        """PAID -> REFUNDED."""
        if self._status != Payment.STATUS_PAID:
            raise InvalidCargoStateException(
                title=f"Payment {self._amount}",
                state=self._status,
                reason="Cannot refund a payment that is not paid",
            )
        self._status = Payment.STATUS_REFUNDED
        return True

    def verify(self) -> bool:
        """Return True if the payment is paid."""
        return self._status == Payment.STATUS_PAID
