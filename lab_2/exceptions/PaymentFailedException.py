from exceptions.MuseumException import MuseumException


class PaymentFailedException(MuseumException):

    def __init__(self, amount: float = None, method: str = None, reason: str = None):
        message = "Payment failed"
        if reason:
            message = f"Payment failed: {reason}"
        elif amount is not None:
            message = f"Payment for {amount} failed"
            if method:
                message += f" ({method})"
        super().__init__(message, error_code="PAYMENT_FAILED")
        self._amount = amount
        self._method = method
        self._reason = reason

    @property
    def amount(self):
        return self._amount

    @property
    def method(self):
        return self._method

    @property
    def reason(self):
        return self._reason