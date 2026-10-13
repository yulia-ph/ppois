from exceptions.MuseumException import MuseumException


class RestorationException(MuseumException):

    def __init__(self, reason: str = "It is impossible to restore"):
        super().__init__(reason, error_code="RESTORATION_ERROR")
        self._reason = reason

    @property
    def reason(self):
        return self._reason