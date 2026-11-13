from datetime import date

from exceptions.InvalidCargoStateException import InvalidCargoStateException


class Incident:
    """An accident or event involving a vehicle and driver."""

    TYPE_ACCIDENT = "accident"
    TYPE_BREAKDOWN = "breakdown"
    TYPE_THEFT = "theft"

    VALID_TYPES = (TYPE_ACCIDENT, TYPE_BREAKDOWN, TYPE_THEFT)

    _counter = 0

    def __init__(self, type_: str, place: str, severity: int, vehicle, driver):
        if type_ not in Incident.VALID_TYPES:
            raise ValueError(f"Invalid incident type '{type_}'")
        if not place:
            raise ValueError("Place must not be empty")
        if not 1 <= severity <= 5:
            raise ValueError("Severity must be between 1 and 5")
        if vehicle is None or driver is None:
            raise ValueError("Vehicle and driver must not be None")
        Incident._counter += 1
        self._id = f"INC-{Incident._counter:04d}"
        self._type = type_
        self._place = place
        self._severity = severity
        self._date = date.today()
        self._vehicle = vehicle
        self._driver = driver
        self._evidence = []
        self._order = None
        self._is_open = True

    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return self._type

    @property
    def place(self):
        return self._place

    @property
    def severity(self):
        return self._severity

    @property
    def date(self):
        return self._date

    @property
    def vehicle(self):
        return self._vehicle

    @property
    def driver(self):
        return self._driver

    def add_evidence(self, note: str):
        """Attach evidence while the incident is open."""
        if not note:
            raise ValueError("Evidence must not be empty")
        if not self._is_open:
            raise InvalidCargoStateException(
                title=self._id,
                state="closed",
                reason="Cannot add evidence to a closed incident",
            )
        self._evidence.append(note)
        return True

    def close(self):
        """Close the incident."""
        if not self._is_open:
            raise InvalidCargoStateException(
                title=self._id,
                state="closed",
                reason="Incident is already closed",
            )
        self._is_open = False
        return True

    def is_open(self) -> bool:
        """Return True if the incident is still open."""
        return self._is_open

    def link_order(self, order):
        """Link a shipment order."""
        if order is None:
            raise ValueError("Order must not be None")
        self._order = order
        return True
