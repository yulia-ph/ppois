from exceptions.LogisticsException import LogisticsException


class VehicleOverloadException(LogisticsException):

    def __init__(self, plate: str = None, weight: float = None, capacity: float = None):
        message = "The vehicle is overloaded"
        if plate:
            message = f"Vehicle «{plate}» is overloaded"
            if weight is not None and capacity is not None:
                message += f" ({weight} > {capacity})"
        super().__init__(message, error_code="VEHICLE_OVERLOAD")
        self._plate = plate
        self._weight = weight
        self._capacity = capacity

    @property
    def plate(self):
        return self._plate

    @property
    def weight(self):
        return self._weight

    @property
    def capacity(self):
        return self._capacity
