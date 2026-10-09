from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
from museum_people.Employee import Employee


class SecurityGuard(Employee):
    """A museum security guard.

    Guards patrol an assigned zone, check access for visitors and
    staff, log every access attempt, and report incidents. Each guard
    keeps a journal of access records and a list of incidents they
    are responsible for.
    """

    VALID_SEVERITIES = ("low", "medium", "high")

    def __init__(self, name: str, salary: float, hire_date,
                 shift: str, zone: str):
        """Initialize a security guard.

        Args:
            name: Employee name. Must not be empty.
            salary: Monthly salary. Must be non-negative.
            hire_date: Date of hire. Must not be None.
            shift: Shift label (e.g. "day", "night"). Must not be empty.
            zone: Assigned zone. Must not be empty.

        Raises:
            ValueError: If inherited validation fails, or shift/zone is
                empty.
        """
        super().__init__(name, salary, hire_date)
        if not shift:
            raise ValueError("Shift must not be empty")
        if not zone:
            raise ValueError("Zone must not be empty")
        self._shift = shift
        self._zone = zone
        self._journal = []
        self._incidents = []


    @property
    def shift(self):
        return self._shift

    @property
    def zone(self):
        return self._zone

    @property
    def journal(self):
        return list(self._journal)

    @property
    def incidents(self):
        return list(self._incidents)


    def check_access(self, person, zone) -> bool:
        """Check whether a person may enter a zone, and log the attempt.

        Args:
            person: The person attempting to enter. Must not be None.
            zone: The target zone. Must not be empty.

        Returns:
            True if access was granted.

        Raises:
            ValueError: If person is None or zone is empty.
        """
        if person is None:
            raise ValueError("Person must not be None")
        if not zone:
            raise ValueError("Zone must not be empty")

        from museum_security.AccessControl import AccessControl
        record = AccessControl(person, zone)
        record.check_access()
        self._journal.append(record)
        return record.is_granted


    def report_incident(self, type_: str, place: str,
                        severity: str = "medium"):
        """Create and assign a new incident to this guard.

        Args:
            type_: Incident type (e.g. "theft", "vandalism"). Must not
                be empty.
            place: Where the incident occurred. Must not be empty.
            severity: One of VALID_SEVERITIES.

        Returns:
            The newly created Incident.

        Raises:
            ValueError: If type_ or place is empty, or severity is not
                valid.
        """
        if not type_:
            raise ValueError("Incident type must not be empty")
        if not place:
            raise ValueError("Incident place must not be empty")
        if severity not in SecurityGuard.VALID_SEVERITIES:
            raise ValueError(
                f"Severity must be one of {SecurityGuard.VALID_SEVERITIES}, "
                f"got '{severity}'"
            )

        from museum_security.Incident import Incident
        incident = Incident(type_, place, severity)
        incident.assign_guard(self)
        self._incidents.append(incident)
        return incident

    def close_incident(self, incident):
        """Close an incident.

        Args:
            incident: The incident to close. Must not be None.

        Returns:
            True on success.

        Raises:
            ValueError: If incident is None.
            InvalidExhibitStateException: If the incident could not be
                closed (e.g. no evidence, no assigned guard, already closed).
        """
        if incident is None:
            raise ValueError("Incident must not be None")
        if not incident.close_incident():
            raise InvalidExhibitStateException(
                exhibit_title=incident.id,
                state="cannot_close",
                reason="Incident could not be closed",
            )
        return True

    def get_open_incidents(self) -> list:
        """Return all incidents assigned to this guard that are not closed."""
        return [i for i in self._incidents if not i.is_closed]