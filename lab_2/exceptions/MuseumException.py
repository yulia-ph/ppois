class MuseumException(Exception):

    def __init__(self, message: str = "A mistake in the museum's work", error_code: str = None):
        super().__init__(message)
        self._message = message
        self._error_code = error_code or self.__class__.__name__

    @property
    def message(self):
        return self._message

    @property
    def error_code(self):
        return self._error_code

    def __str__(self):
        return f"[{self._error_code}] {self._message}"