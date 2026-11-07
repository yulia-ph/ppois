from exceptions.LogisticsException import LogisticsException


class CargoOverweightException(LogisticsException):

    def __init__(self, weight: float = None, limit: float = None):
        message = "The cargo is too heavy"
        if weight is not None and limit is not None:
            message = f"Weight {weight} exceeds limit {limit}"
        super().__init__(message, error_code="CARGO_OVERWEIGHT")
        self._weight = weight
        self._limit = limit

    @property
    def weight(self):
        return self._weight

    @property
    def limit(self):
        return self._limit
