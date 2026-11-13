from exceptions.LogisticsException import LogisticsException


class InvalidCargoStateException(LogisticsException):

    def __init__(self, title: str = None, state: str = None, reason: str = None):
        message = "The object is in an unacceptable state"
        if title and state:
            message = f"«{title}» is in state {state}"
        if reason:
            message += f": {reason}"
        super().__init__(message, error_code="INVALID_CARGO_STATE")
        self._title = title
        self._state = state
        self._reason = reason

    @property
    def title(self):
        return self._title

    @property
    def state(self):
        return self._state

    @property
    def reason(self):
        return self._reason
