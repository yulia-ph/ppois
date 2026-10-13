from exceptions.MuseumException import MuseumException


class BookingConflictException(MuseumException):

    def __init__(self, reason: str = "Booking conflict"):
        super().__init__(reason, error_code="BOOKING_CONFLICT")
        self._reason = reason

    @property
    def reason(self):
        return self._reason