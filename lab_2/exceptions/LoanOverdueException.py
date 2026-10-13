from exceptions.MuseumException import MuseumException


class LoanOverdueException(MuseumException):

    def __init__(self, days_overdue: int = 0):
        message = "Delayed return of the exhibit"
        if days_overdue > 0:
            message = f"Refund delay: {days_overdue} days"
        super().__init__(message, error_code="LOAN_OVERDUE")
        self._days_overdue = days_overdue

    @property
    def days_overdue(self):
        return self._days_overdue