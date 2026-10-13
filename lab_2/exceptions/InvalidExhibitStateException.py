from exceptions.MuseumException import MuseumException


class InvalidExhibitStateException(MuseumException):

    def __init__(self, exhibit_title: str = None, state: str = None, reason: str = None):
        message = "The exhibit is in an unacceptable condition"
        if exhibit_title and state:
            message = f"Exhibit «{exhibit_title}» is in condition {state}"
        if reason:
            message += f": {reason}"
        super().__init__(message, error_code="INVALID_EXHIBIT_STATE")
        self._exhibit_title = exhibit_title
        self._state = state
        self._reason = reason

    @property
    def exhibit_title(self):
        return self._exhibit_title

    @property
    def state(self):
        return self._state

    @property
    def reason(self):
        return self._reason