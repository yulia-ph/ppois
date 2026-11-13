from exceptions.LogisticsException import LogisticsException


class InvalidLicenseException(LogisticsException):

    def __init__(self, number: str = None, reason: str = None):
        message = "The driving license is not valid"
        if number:
            message = f"License «{number}» is not valid"
        if reason:
            message += f": {reason}"
        super().__init__(message, error_code="INVALID_LICENSE")
        self._number = number
        self._reason = reason

    @property
    def number(self):
        return self._number

    @property
    def reason(self):
        return self._reason
