from exceptions.MuseumException import MuseumException


class LoanAlreadyActiveException(MuseumException):

    def __init__(self, exhibit_title: str = None):
        message = "The exhibit has already been issued"
        if exhibit_title:
            message = f"The exhibit «{exhibit_title}» has already been issued"
        super().__init__(message, error_code="LOAN_ALREADY_ACTIVE")
        self._exhibit_title = exhibit_title

    @property
    def exhibit_title(self):
        return self._exhibit_title