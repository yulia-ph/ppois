from exceptions.Lab4Exception import Lab4Exception


class InvalidIteratorException(Lab4Exception):
    """Raised when an iterator is used incorrectly."""

    def __init__(self, reason: str = "Iterator is not on an element"):
        super().__init__(message=reason, error_code="INVALID_ITERATOR")
