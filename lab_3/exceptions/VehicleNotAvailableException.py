from exceptions.LogisticsException import LogisticsException


class VehicleNotAvailableException(LogisticsException):

    def __init__(self, plate: str = None, status: str = None):
        message = "The vehicle is not available"
        if plate:
            message = f"Vehicle «{plate}» is not available"
            if status:
                message += f" (status: {status})"
        super().__init__(message, error_code="VEHICLE_NOT_AVAILABLE")
        self._plate = plate
        self._status = status

    @property
    def plate(self):
        return self._plate

    @property
    def status(self):
        return self._status
