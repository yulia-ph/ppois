from exceptions.LogisticsException import LogisticsException


class RouteConflictException(LogisticsException):

    def __init__(self, reason: str = None):
        message = "Route or trip conflict"
        if reason:
            message = f"Route conflict: {reason}"
        super().__init__(message, error_code="ROUTE_CONFLICT")
        self._reason = reason

    @property
    def reason(self):
        return self._reason
