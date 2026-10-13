from datetime import datetime

from exceptions.InvalidExhibitStateException import InvalidExhibitStateException


class Incident:
    """A museum incident: theft, vandalism, fire, flood, medical, other.

    An incident is an open case until it is closed. To close an
    incident it must have an assigned guard and at least one piece of
    evidence.

    Related exhibits (e.g. those damaged in the incident) can be linked
    to the incident for record-keeping.
    """

    TYPE_THEFT = "theft"
    TYPE_VANDALISM = "vandalism"
    TYPE_FIRE = "fire"
    TYPE_FLOOD = "flood"
    TYPE_MEDICAL = "medical"
    TYPE_OTHER = "other"

    VALID_TYPES = (
        TYPE_THEFT,
        TYPE_VANDALISM,
        TYPE_FIRE,
        TYPE_FLOOD,
        TYPE_MEDICAL,
        TYPE_OTHER,
    )

    SEVERITY_LOW = "low"
    SEVERITY_MEDIUM = "medium"
    SEVERITY_HIGH = "high"

    VALID_SEVERITIES = (SEVERITY_LOW, SEVERITY_MEDIUM, SEVERITY_HIGH)

    _counter = 0

    def __init__(self, type_: str, place: str, severity: str = "medium"):
        """Initialize an incident.

        Args:
            type_: One of VALID_TYPES.
            place: Where the incident occurred. Must not be empty.
            severity: One of VALID_SEVERITIES.

        Raises:
            ValueError: If any argument is invalid.
        """
        if type_ not in Incident.VALID_TYPES:
            raise ValueError(
                f"Invalid incident type '{type_}'. "
                f"Must be one of {Incident.VALID_TYPES}"
            )
        if not place:
            raise ValueError("Incident place must not be empty")
        if severity not in Incident.VALID_SEVERITIES:
            raise ValueError(
                f"Invalid severity '{severity}'. "
                f"Must be one of {Incident.VALID_SEVERITIES}"
            )

        Incident._counter += 1
        self._id = f"INC-{Incident._counter:04d}"
        self._type = type_
        self._place = place
        self._severity = severity
        self._date = datetime.now()
        self._is_closed = False
        self._guard = None
        self._evidence = []
        self._related_exhibits = []


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
    def is_closed(self):
        return self._is_closed

    @property
    def guard(self):
        return self._guard

    @property
    def evidence(self):
        return list(self._evidence)

    @property
    def related_exhibits(self):
        return list(self._related_exhibits)


    def assign_guard(self, guard):
        """Assign a security guard as responsible for this incident.

        Args:
            guard: The guard. Must not be None.

        Raises:
            ValueError: If guard is None.
            InvalidExhibitStateException: If the incident is already closed.
        """
        if guard is None:
            raise ValueError("Guard must not be None")
        if self._is_closed:
            raise InvalidExhibitStateException(
                exhibit_title=self._id,
                state="closed",
                reason="Cannot assign a guard to a closed incident",
            )
        self._guard = guard
        return True


    def add_evidence(self, text: str):
        """Add a piece of evidence (witness statement, note, etc.).

        Args:
            text: The evidence text. Must not be empty.

        Raises:
            ValueError: If text is empty.
            InvalidExhibitStateException: If the incident is already closed.
        """
        if not text:
            raise ValueError("Evidence text must not be empty")
        if self._is_closed:
            raise InvalidExhibitStateException(
                exhibit_title=self._id,
                state="closed",
                reason="Cannot add evidence to a closed incident",
            )
        self._evidence.append(text)
        return True


    def link_exhibit(self, exhibit):
        """Link an exhibit to this incident.

        Idempotent: linking an already linked exhibit is not an error.

        Args:
            exhibit: The exhibit to link. Must not be None.

        Raises:
            ValueError: If exhibit is None.
        """
        if exhibit is None:
            raise ValueError("Exhibit must not be None")
        if exhibit not in self._related_exhibits:
            self._related_exhibits.append(exhibit)
        return True


    def investigate(self) -> bool:
        """Return True if the incident has everything needed to close.

        Requirements: an assigned guard and at least one piece of
        evidence. Closed incidents always return False.
        """
        if self._is_closed:
            return False
        if self._guard is None:
            return False
        return bool(self._evidence)

    def close_incident(self):
        """Close the incident.

        Raises:
            InvalidExhibitStateException: If the incident cannot be
                closed (already closed, no guard, or no evidence).
        """
        if self._is_closed:
            raise InvalidExhibitStateException(
                exhibit_title=self._id,
                state="closed",
                reason="Incident is already closed",
            )
        if not self.investigate():
            raise InvalidExhibitStateException(
                exhibit_title=self._id,
                state="open",
                reason="Cannot close an incident without a guard and evidence",
            )
        self._is_closed = True
        return True