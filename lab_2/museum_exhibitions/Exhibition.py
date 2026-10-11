from exceptions.InvalidExhibitStateException import InvalidExhibitStateException


class Exhibition:
    """A museum exhibition.

    An exhibition has a title, date range, a curator, and a collection
    of exhibits. It can be opened and closed; tickets sold for the
    exhibition are tracked here for revenue reporting.

    The exhibition does not own its exhibits — it only references
    them. An exhibit can be removed from an exhibition without being
    removed from its collection or storage.
    """

    TYPE_PERMANENT = "permanent"
    TYPE_TEMPORARY = "temporary"
    TYPE_MIXED = "mixed"

    VALID_TYPES = (TYPE_PERMANENT, TYPE_TEMPORARY, TYPE_MIXED)

    _counter = 0

    def __init__(self, title: str, start_date, end_date, curator,
                 type_: str = "permanent"):
        """Initialize an exhibition.

        Args:
            title: The exhibition title. Must not be empty.
            start_date: Start date. Must not be None.
            end_date: End date. Must be after start_date.
            curator: The curator responsible. Must not be None.
            type_: One of VALID_TYPES.

        Raises:
            ValueError: If any argument is invalid.
        """
        if not title:
            raise ValueError("Exhibition title must not be empty")
        if start_date is None:
            raise ValueError("Start date must not be None")
        if end_date is None:
            raise ValueError("End date must not be None")
        if end_date <= start_date:
            raise ValueError(
                f"End date {end_date} must be after start date {start_date}"
            )
        if curator is None:
            raise ValueError("Curator must not be None")
        if type_ not in Exhibition.VALID_TYPES:
            raise ValueError(
                f"Invalid exhibition type '{type_}'. "
                f"Must be one of {Exhibition.VALID_TYPES}"
            )

        Exhibition._counter += 1
        self._id = f"EXH-{Exhibition._counter:04d}"
        self._title = title
        self._start_date = start_date
        self._end_date = end_date
        self._curator = curator
        self._type = type_
        self._exhibits = []
        self._tickets = []
        self._is_open = False

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def curator(self):
        return self._curator

    @property
    def type(self):
        return self._type

    @property
    def exhibits(self):
        return list(self._exhibits)

    @property
    def tickets(self):
        return list(self._tickets)

    @property
    def is_open(self):
        return self._is_open


    def add_exhibit(self, exhibit):
        """Add an exhibit to the exhibition.

        Args:
            exhibit: The exhibit. Must not be None and must be
                available for exhibition.

        Raises:
            ValueError: If exhibit is None or already in the exhibition.
            InvalidExhibitStateException: If the exhibit's condition
                does not allow it to be displayed.
        """
        if exhibit is None:
            raise ValueError("Exhibit must not be None")
        if exhibit in self._exhibits:
            raise ValueError(
                f"Exhibit '{exhibit.inventory_number}' is already in "
                f"exhibition '{self._title}'"
            )
        if not exhibit.is_available_for_exhibition():
            raise InvalidExhibitStateException(
                exhibit_title=exhibit.title,
                state=exhibit.condition,
                reason="Exhibit is not available for exhibition",
            )
        self._exhibits.append(exhibit)
        return True

    def remove_exhibit(self, exhibit):
        """Remove an exhibit from the exhibition.

        Args:
            exhibit: The exhibit. Must be in the exhibition.

        Raises:
            ValueError: If exhibit is None or not present.
        """
        if exhibit is None:
            raise ValueError("Exhibit must not be None")
        if exhibit not in self._exhibits:
            raise ValueError(
                f"Exhibit '{exhibit.inventory_number}' is not in "
                f"exhibition '{self._title}'"
            )
        self._exhibits.remove(exhibit)
        return True

    def count_exhibits(self) -> int:
        """Return the number of exhibits in the exhibition."""
        return len(self._exhibits)


    def open(self):
        """Open the exhibition for visitors.

        Idempotent: opening an already open exhibition is not an error.
        """
        self._is_open = True
        return True

    def close(self):
        """Close the exhibition.

        Idempotent: closing an already closed exhibition is not an error.
        """
        self._is_open = False
        return True

    def extend_dates(self, new_end):
        """Extend the exhibition's end date.

        Args:
            new_end: New end date. Must be after the current end date.

        Raises:
            ValueError: If new_end is None or not after the current end.
        """
        if new_end is None:
            raise ValueError("New end date must not be None")
        if new_end <= self._end_date:
            raise ValueError(
                f"New end date {new_end} must be after current end "
                f"{self._end_date}"
            )
        self._end_date = new_end
        return True

    def duration_days(self) -> int:
        """Return the exhibition's duration in days."""
        return (self._end_date - self._start_date).days


    def add_ticket(self, ticket):
        """Add a sold ticket to this exhibition.

        Args:
            ticket: The ticket. Must not be None.

        Raises:
            ValueError: If ticket is None or already in the exhibition.
        """
        if ticket is None:
            raise ValueError("Ticket must not be None")
        if ticket in self._tickets:
            raise ValueError(
                f"Ticket '{ticket.number}' is already registered for "
                f"exhibition '{self._title}'"
            )
        self._tickets.append(ticket)
        return True

    def calculate_tickets_sold(self) -> int:
        """Return the number of tickets sold for this exhibition."""
        return len(self._tickets)

    def calculate_revenue(self) -> float:
        """Return the total revenue from tickets sold."""
        return sum(t.cost for t in self._tickets)

    def change_curator(self, new_curator):
        """Replace the exhibition's curator.

        Only allowed while the exhibition is closed.

        Args:
            new_curator: The new curator. Must not be None.

        Raises:
            ValueError: If new_curator is None.
            InvalidExhibitStateException: If the exhibition is open.
        """
        if new_curator is None:
            raise ValueError("Curator must not be None")
        if self._is_open:
            raise InvalidExhibitStateException(
                exhibit_title=self._title,
                state="open",
                reason="Cannot change curator of an open exhibition",
            )
        self._curator = new_curator
        return True