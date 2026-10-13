from datetime import date

from exceptions.InvalidExhibitStateException import InvalidExhibitStateException


class Loan:
    """A loan of an exhibit to another institution.

    A loan moves through states:

        PENDING -> APPROVED -> RETURNED
                    |
                    v
                OVERDUE

    The exhibit must be available for exhibition before approval.
    Extending a loan updates the end date; a loan becomes overdue if
    today's date passes the end date while still approved.
    """

    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_RETURNED = "returned"
    STATUS_OVERDUE = "overdue"

    def __init__(self, exhibit, borrower: str, start_date: date, end_date: date):
        """Initialize a loan.

        Args:
            exhibit: The exhibit being loaned. Must not be None.
            borrower: The borrowing institution. Must not be empty.
            start_date: Loan start date. Must not be None.
            end_date: Loan end date. Must be after start_date.

        Raises:
            ValueError: If any argument is invalid.
        """
        if exhibit is None:
            raise ValueError("Exhibit must not be None")
        if not borrower:
            raise ValueError("Borrower must not be empty")
        if start_date is None:
            raise ValueError("Start date must not be None")
        if end_date is None:
            raise ValueError("End date must not be None")
        if end_date <= start_date:
            raise ValueError(
                f"End date {end_date} must be after start date {start_date}"
            )

        self._exhibit = exhibit
        self._borrower = borrower
        self._start_date = start_date
        self._end_date = end_date
        self._status = Loan.STATUS_PENDING
        self._return_condition = None
        self._returned_date = None


    @property
    def exhibit(self):
        return self._exhibit

    @property
    def borrower(self):
        return self._borrower

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def status(self):
        return self._status

    @property
    def return_condition(self):
        return self._return_condition

    @property
    def returned_date(self):
        return self._returned_date

    @property
    def is_active(self):
        return self._status == Loan.STATUS_APPROVED

    @property
    def is_returned(self):
        return self._status == Loan.STATUS_RETURNED

    @property
    def is_overdue_status(self):
        return self._status == Loan.STATUS_OVERDUE


    def approve_loan(self):
        """Approve the loan request.

        Raises:
            InvalidExhibitStateException: If the loan is not pending, or
                the exhibit is not available for exhibition.
        """
        if self._status != Loan.STATUS_PENDING:
            raise InvalidExhibitStateException(
                exhibit_title=self._exhibit.inventory_number,
                state=self._status,
                reason="Cannot approve a loan that is not pending",
            )
        if not self._exhibit.is_available_for_exhibition():
            raise InvalidExhibitStateException(
                exhibit_title=self._exhibit.title,
                state=self._exhibit.condition,
                reason="Exhibit is not available for loan",
            )
        self._status = Loan.STATUS_APPROVED
        return True


    def return_exhibit(self):
        """Mark the exhibit as returned.

        Raises:
            InvalidExhibitStateException: If the loan is not approved
                or already returned.
        """
        if self._status == Loan.STATUS_RETURNED:
            raise InvalidExhibitStateException(
                exhibit_title=self._exhibit.inventory_number,
                state="returned",
                reason="Exhibit has already been returned",
            )
        if self._status != Loan.STATUS_APPROVED:
            raise InvalidExhibitStateException(
                exhibit_title=self._exhibit.inventory_number,
                state=self._status,
                reason="Cannot return an exhibit from a loan that is not approved",
            )
        self._status = Loan.STATUS_RETURNED
        self._returned_date = date.today()
        return True

    def register_return(self, condition: str):
        """Record the exhibit's condition upon return.

        Args:
            condition: Description of the return condition. Must not
                be empty.

        Raises:
            ValueError: If condition is empty.
            InvalidExhibitStateException: If the loan is not returned yet.
        """
        if not condition:
            raise ValueError("Return condition must not be empty")
        if self._status != Loan.STATUS_RETURNED:
            raise InvalidExhibitStateException(
                exhibit_title=self._exhibit.inventory_number,
                state=self._status,
                reason="Cannot register return before the exhibit is returned",
            )
        self._return_condition = condition
        return True


    def extend_loan(self, new_end_date: date):
        """Extend the loan's end date.

        Args:
            new_end_date: New end date. Must be after the current one.

        Raises:
            ValueError: If new_end_date is None or not after the current one.
            InvalidExhibitStateException: If the loan has been returned.
        """
        if new_end_date is None:
            raise ValueError("New end date must not be None")
        if new_end_date <= self._end_date:
            raise ValueError(
                f"New end date {new_end_date} must be after current "
                f"{self._end_date}"
            )
        if self._status == Loan.STATUS_RETURNED:
            raise InvalidExhibitStateException(
                exhibit_title=self._exhibit.inventory_number,
                state="returned",
                reason="Cannot extend a returned loan",
            )
        self._end_date = new_end_date
        return True


    def is_overdue(self, today: date = None) -> bool:
        """Return True if the loan is currently overdue.

        Only APPROVED loans can be overdue.
        """
        if today is None:
            today = date.today()
        if self._status != Loan.STATUS_APPROVED:
            return False
        return today > self._end_date
