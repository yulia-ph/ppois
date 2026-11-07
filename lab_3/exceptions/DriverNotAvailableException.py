from exceptions.LogisticsException import LogisticsException


class DriverNotAvailableException(LogisticsException):

    def __init__(self, name: str = None, reason: str = None):
        message = "The driver is not available"
        if name:
            message = f"Driver «{name}» is not available"
        if reason:
            message += f": {reason}"
        super().__init__(message, error_code="DRIVER_NOT_AVAILABLE")
        self._name = name
        self._reason = reason

    @property
    def name(self):
        return self._name

    @property
    def reason(self):
        return self._reason
