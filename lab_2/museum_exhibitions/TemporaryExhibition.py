from museum_exhibitions.Exhibition import Exhibition


class TemporaryExhibition(Exhibition):
    """A temporary (loan-based) exhibition.

    Extends Exhibition with a theme and a list of loans: exhibits
    borrowed from other institutions or from other parts of the
    museum for the duration of the exhibition.
    """

    def __init__(self, title, start_date, end_date, curator, theme: str):
        """Initialize a temporary exhibition.

        Args:
            title: The exhibition title.
            start_date: Start date.
            end_date: End date (must be after start_date).
            curator: The curator.
            theme: Thematic focus. Must not be empty.

        Raises:
            ValueError: If theme is empty or inherited validation fails.
        """
        if not theme:
            raise ValueError("Theme must not be empty")
        super().__init__(title, start_date, end_date, curator,
                         type_=Exhibition.TYPE_TEMPORARY)
        self._theme = theme
        self._loans = []


    @property
    def theme(self):
        return self._theme

    @property
    def loans(self):
        return list(self._loans)

    def add_loan(self, loan):
        """Register a loan with this exhibition.

        Args:
            loan: The loan. Must not be None and must not already be
                registered.

        Raises:
            ValueError: If loan is None or already present.
        """
        if loan is None:
            raise ValueError("Loan must not be None")
        if loan in self._loans:
            raise ValueError("Loan is already registered for this exhibition")
        self._loans.append(loan)
        return True

    def remove_loan(self, loan):
        """Unregister a loan from this exhibition.

        Args:
            loan: The loan. Must be present.

        Raises:
            ValueError: If loan is None or not present.
        """
        if loan is None:
            raise ValueError("Loan must not be None")
        if loan not in self._loans:
            raise ValueError("Loan is not registered for this exhibition")
        self._loans.remove(loan)
        return True

    def return_loans(self) -> int:
        """Return all currently active loans.

        Calls `return_exhibit()` on each loan. Returns the number of
        loans that were successfully returned. Loans are NOT removed
        from the list — they stay as historical records.
        """
        returned = 0
        for loan in self._loans:
            if loan.return_exhibit():
                returned += 1
        return returned

    def check_loans_overdue(self) -> list:
        """Return all loans that are overdue."""
        return [loan for loan in self._loans if loan.is_overdue()]