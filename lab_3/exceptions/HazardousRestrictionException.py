from exceptions.LogisticsException import LogisticsException


class HazardousRestrictionException(LogisticsException):

    def __init__(self, reason: str = None):
        message = "Hazardous cargo restriction"
        if reason:
            message = f"Hazardous restriction: {reason}"
        super().__init__(message, error_code="HAZARDOUS_RESTRICTION")
        self._reason = reason

    @property
    def reason(self):
        return self._reason
