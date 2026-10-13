from datetime import date


class Report:
    """A generated report about museum activity.

    Reports have a period, a type, and a data dict built up by
    `generate` and `add_section`. They can be exported to a string
    in one of several formats. Reports are not inherently tied to any
    particular domain object — the type and data define their meaning.
    """

    TYPE_ANNUAL = "annual"
    TYPE_FINANCIAL = "financial"
    TYPE_ATTENDANCE = "attendance"
    TYPE_RESTORATION = "restoration"
    TYPE_INVENTORY = "inventory"

    VALID_TYPES = (
        TYPE_ANNUAL,
        TYPE_FINANCIAL,
        TYPE_ATTENDANCE,
        TYPE_RESTORATION,
        TYPE_INVENTORY,
    )

    VALID_FORMATS = ("pdf", "excel", "txt")

    _counter = 0

    def __init__(self, period: str, type_: str):
        """Initialize a report.

        Args:
            period: Report period description (e.g. "2025", "Q1 2025").
                Must not be empty.
            type_: One of VALID_TYPES.

        Raises:
            ValueError: If period is empty or type_ is invalid.
        """
        if not period:
            raise ValueError("Period must not be empty")
        if type_ not in Report.VALID_TYPES:
            raise ValueError(
                f"Invalid report type '{type_}'. Must be one of {Report.VALID_TYPES}"
            )

        Report._counter += 1
        self._id = f"REP-{Report._counter:04d}"
        self._period = period
        self._type = type_
        self._data = {}
        self._created_date = date.today()
        self._author = None


    @property
    def id(self):
        return self._id

    @property
    def period(self):
        return self._period

    @property
    def type(self):
        return self._type

    @property
    def data(self):
        return dict(self._data)

    @property
    def created_date(self):
        return self._created_date

    @property
    def author(self):
        return self._author


    def set_author(self, author):
        """Set the report author.

        Args:
            author: The author. Must not be None.

        Raises:
            ValueError: If author is None.
        """
        if author is None:
            raise ValueError("Author must not be None")
        self._author = author
        return True


    def generate(self, data: dict):
        """Fill the report with data.

        Args:
            data: A dict of report data. Must be a dict.

        Raises:
            ValueError: If data is not a dict.
        """
        if not isinstance(data, dict):
            raise TypeError(
                f"Data must be a dict, got {type(data).__name__}"
            )
        self._data.update(data)
        return True

    def add_section(self, key: str, value):
        """Add or overwrite a single section of the report.

        Args:
            key: Section key. Must not be empty.
            value: Section value (any type).

        Raises:
            ValueError: If key is empty.
        """
        if not key:
            raise ValueError("Section key must not be empty")
        self._data[key] = value
        return True

    def is_empty(self) -> bool:
        """Return True if the report has no data."""
        return len(self._data) == 0


    def export(self, format_: str) -> str:
        """Export the report as a string in the given format.

        Args:
            format_: One of VALID_FORMATS.

        Returns:
            A string representation of the report.

        Raises:
            ValueError: If format_ is not supported.
        """
        if format_ not in Report.VALID_FORMATS:
            raise ValueError(
                f"Unsupported format '{format_}'. "
                f"Must be one of {Report.VALID_FORMATS}"
            )
        return f"[{format_}] {self._id}: {self._data}"

    def to_string(self) -> str:
        """Return a human-readable summary string."""
        return f"Report {self._id} ({self._type}, {self._period}): {self._data}"