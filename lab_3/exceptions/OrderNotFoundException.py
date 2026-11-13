from exceptions.LogisticsException import LogisticsException


class OrderNotFoundException(LogisticsException):

    def __init__(self, number: str = None):
        message = "The shipment order was not found"
        if number:
            message = f"Order «{number}» was not found"
        super().__init__(message, error_code="ORDER_NOT_FOUND")
        self._number = number

    @property
    def number(self):
        return self._number
