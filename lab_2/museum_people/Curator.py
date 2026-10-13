from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
from exceptions.LoanOverdueException import LoanOverdueException
from museum_people.Employee import Employee


class Curator(Employee):
    """A museum curator.

    Curators manage collections and create exhibitions. They also
    approve loans of exhibits to other institutions. The curator keeps
    references to the collections they curate and exhibitions they
    have created.
    """

    VALID_EXHIBITION_TYPES = ("permanent", "temporary", "mixed")

    def __init__(self, name: str, salary: float, hire_date, specialization: str):
        """Initialize a curator.

        Args:
            name: Employee name. Must not be empty.
            salary: Monthly salary. Must be non-negative.
            hire_date: Date of hire. Must not be None.
            specialization: The area of expertise. Must not be empty.

        Raises:
            ValueError: If inherited validation fails or specialization
                is empty.
        """
        super().__init__(name, salary, hire_date)
        if not specialization:
            raise ValueError("Specialization must not be empty")
        self._specialization = specialization
        self._collections = []
        self._exhibitions = []


    @property
    def specialization(self):
        return self._specialization

    @property
    def collections(self):
        return list(self._collections)

    @property
    def exhibitions(self):
        return list(self._exhibitions)


    def curate_collection(self, collection):
        """Assign a collection to this curator.

        Args:
            collection: The collection to curate. Must not be None.

        Raises:
            ValueError: If collection is None or already curated.
        """
        if collection is None:
            raise ValueError("Collection must not be None")
        if collection in self._collections:
            raise ValueError(
                f"Collection '{collection.name}' is already curated "
                f"by {self._name}"
            )
        self._collections.append(collection)
        return True


    def create_exhibition(self, title: str, start, end,
                          exhibition_type: str = "permanent"):
        """Create a new exhibition.

        Args:
            title: The exhibition title. Must not be empty.
            start: Start date. Must not be None.
            end: End date. Must be after start.
            exhibition_type: One of VALID_EXHIBITION_TYPES.

        Returns:
            The newly created Exhibition.

        Raises:
            ValueError: If any argument is invalid.
        """
        if not title:
            raise ValueError("Exhibition title must not be empty")
        if start is None:
            raise ValueError("Start date must not be None")
        if end is None:
            raise ValueError("End date must not be None")
        if end <= start:
            raise ValueError(
                f"End date {end} must be after start date {start}"
            )
        if exhibition_type not in Curator.VALID_EXHIBITION_TYPES:
            raise ValueError(
                f"Invalid exhibition type '{exhibition_type}'. "
                f"Must be one of {Curator.VALID_EXHIBITION_TYPES}"
            )
        from museum_exhibitions.Exhibition import Exhibition
        exhibition = Exhibition(title, start, end, self, exhibition_type)
        self._exhibitions.append(exhibition)
        return exhibition


    def select_exhibits(self, collection, count: int = 5) -> list:
        """Select exhibits from a collection for an exhibition.

        Only exhibits that are available for exhibition are returned,
        up to `count` items.

        Args:
            collection: The source collection. Must not be None.
            count: Maximum number of exhibits. Must be positive.

        Returns:
            A list of selected exhibits (possibly empty).

        Raises:
            ValueError: If collection is None or count is not positive.
        """
        if collection is None:
            raise ValueError("Collection must not be None")
        if count <= 0:
            raise ValueError(f"Count must be positive, got {count}")
        selected = []
        for exhibit in collection.exhibits:
            if exhibit.is_available_for_exhibition():
                selected.append(exhibit)
            if len(selected) >= count:
                break
        return selected


    def approve_loan(self, loan):
        """Approve a loan of an exhibit.

        Args:
            loan: The loan to approve. Must not be None.

        Returns:
            True on success.

        Raises:
            ValueError: If loan is None.
            LoanOverdueException: If the loan is already overdue.
            InvalidExhibitStateException: If loan.approve_loan() fails.
        """
        if loan is None:
            raise ValueError("Loan must not be None")
        if loan.is_overdue():
            raise LoanOverdueException()
        if not loan.approve_loan():
            raise InvalidExhibitStateException(
                exhibit_title=f"Loan to {getattr(loan, 'borrower', '?')}",
                state="cannot_approve",
                reason="Loan could not be approved",
            )
        return True