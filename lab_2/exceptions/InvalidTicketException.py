from exceptions.MuseumException import MuseumException


class InvalidTicketException(MuseumException):

    def __init__(self, ticket_number: str = None, reason: str = "The ticket is invalid"):
        message = f"{reason}"
        if ticket_number:
            message = f"Ticket {ticket_number}: {reason}"
        super().__init__(message, error_code="INVALID_TICKET")
        self._ticket_number = ticket_number
        self._reason = reason

    @property
    def ticket_number(self):
        return self._ticket_number

    @property
    def reason(self):
        return self._reason