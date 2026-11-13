from datetime import date


class Report:
    """A generated report."""

    TYPE_ANNUAL = "annual"
    TYPE_FINANCIAL = "financial"
    TYPE_INVENTORY = "inventory"
    TYPE_MAINTENANCE = "maintenance"
    TYPE_INCIDENT = "incident"

    VALID_TYPES = (
        TYPE_ANNUAL,
        TYPE_FINANCIAL,
        TYPE_INVENTORY,
        TYPE_MAINTENANCE,
        TYPE_INCIDENT,
    )

    VALID_FORMATS = ("pdf", "excel", "txt")

    _counter = 0

    def __init__(self, period: str, type_: str):
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
        self._author = None
        self._created_date = date.today()

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
    def author(self):
        return self._author

    @property
    def created_date(self):
        return self._created_date

    def set_author(self, author: str):
        """Set the report author."""
        if not author:
            raise ValueError("Author must not be empty")
        self._author = author
        return True

    def generate(self, data: dict):
        """Replace report data."""
        if data is None:
            raise ValueError("Data must not be None")
        self._data = dict(data)
        return True

    def add_section(self, name: str, value):
        """Add a named section."""
        if not name:
            raise ValueError("Section name must not be empty")
        self._data[name] = value
        return True

    def export(self, fmt: str) -> str:
        """Export as a string in one of VALID_FORMATS."""
        if fmt not in Report.VALID_FORMATS:
            raise ValueError(f"Invalid format '{fmt}'")
        return f"{fmt.upper()}:{self.to_string()}"

    def to_string(self) -> str:
        """Plain-text dump."""
        author = self._author or "unknown"
        return f"{self._id} {self._type} {self._period} by {author} {self._data}"
