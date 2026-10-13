from exceptions.MuseumException import MuseumException


class InsufficientFundsException(MuseumException):

    def __init__(self, required: float = 0.0, available: float = 0.0):
        message = "Insufficient funds"
        if required > 0:
            message = f"Required {required}, available {available}"
        super().__init__(message, error_code="INSUFFICIENT_FUNDS")
        self._required = required
        self._available = available

    @property
    def required(self):
        return self._required

    @property
    def available(self):
        return self._available

    @property
    def shortfall(self):
        return max(0.0, self._required - self._available)