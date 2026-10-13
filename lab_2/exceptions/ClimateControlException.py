from exceptions.MuseumException import MuseumException


class ClimateControlException(MuseumException):

    def __init__(self, temperature: float = None, humidity: float = None):
        message = "Violation of the climate regime"
        details = []
        if temperature is not None:
            details.append(f"T={temperature}°C")
        if humidity is not None:
            details.append(f"H={humidity}%")
        if details:
            message += f" ({', '.join(details)})"
        super().__init__(message, error_code="CLIMATE_VIOLATION")
        self._temperature = temperature
        self._humidity = humidity

    @property
    def temperature(self):
        return self._temperature

    @property
    def humidity(self):
        return self._humidity