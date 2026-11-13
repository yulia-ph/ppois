from exceptions.LogisticsException import LogisticsException


class DeliveryRefusedException(LogisticsException):

    def __init__(self, reason: str = None):
        message = "Delivery was refused"
        if reason:
            message = f"Delivery refused: {reason}"
        super().__init__(message, error_code="DELIVERY_REFUSED")
        self._reason = reason

    @property
    def reason(self):
        return self._reason
