from datetime import datetime

from exceptions.AccessDeniedException import AccessDeniedException


class AccessControl:
    """A single access attempt to a museum zone.

    Represents one attempt by a person (visitor or employee) to enter
    a zone. Zones are divided into public (anyone with a valid ticket)
    and restricted (only employees with the right role).

    The result is recorded on the instance: is_granted + reason. Use
    `check_access()` to ask (returns bool), or `require_access()` to
    enforce (raises AccessDeniedException on denial).
    """

    ZONE_PUBLIC = "public"
    ZONE_STORAGE = "storage"
    ZONE_RESTORATION = "restoration"
    ZONE_ADMIN = "admin"
    ZONE_CASHIER = "cashier"

    VALID_ZONES = (
        ZONE_PUBLIC,
        ZONE_STORAGE,
        ZONE_RESTORATION,
        ZONE_ADMIN,
        ZONE_CASHIER,
    )

    RESTRICTED_ROLES = {
        ZONE_STORAGE: {"Curator", "Restorer", "Administrator"},
        ZONE_RESTORATION: {"Restorer", "Administrator"},
        ZONE_ADMIN: {"Administrator"},
        ZONE_CASHIER: {"Cashier", "Administrator"},
    }

    def __init__(self, person, zone: str):
        """Initialize an access attempt.

        Args:
            person: The person attempting entry. Must not be None.
            zone: The target zone. Must be one of VALID_ZONES.

        Raises:
            ValueError: If person is None or zone is not a known zone.
        """
        if person is None:
            raise ValueError("Person must not be None")
        if zone not in AccessControl.VALID_ZONES:
            raise ValueError(
                f"Unknown zone '{zone}'. "
                f"Must be one of {AccessControl.VALID_ZONES}"
            )
        self._person = person
        self._zone = zone
        self._time = datetime.now()
        self._is_granted = False
        self._reason = None


    @property
    def person(self):
        return self._person

    @property
    def time(self):
        return self._time

    @property
    def zone(self):
        return self._zone

    @property
    def is_granted(self):
        return self._is_granted

    @property
    def reason(self):
        return self._reason


    def check_access(self) -> bool:
        """Decide whether the person may enter the zone.

        Returns True if access was granted, False otherwise. The
        result and reason are stored on this instance.

        The method does not raise on denial — use require_access() if
        you want an exception instead.
        """
        if self._zone == AccessControl.ZONE_PUBLIC:
            return self._check_public_access()
        return self._check_restricted_access()

    def require_access(self):
        """Enforce access: raise on denial.

        Raises:
            AccessDeniedException: If access was not granted.
        """
        self.check_access()
        if not self._is_granted:
            raise AccessDeniedException(
                person_name=getattr(self._person, "name", "unknown"),
                zone=self._zone,
            )
        return True


    def _check_public_access(self) -> bool:
        """Public zones: any person with a valid ticket may enter."""
        ticket = getattr(self._person, "ticket", None)
        if ticket is None:
            return self._deny("No ticket")

        from exceptions.InvalidTicketException import InvalidTicketException
        try:
            ticket.validate()
        except InvalidTicketException as exc:
            return self._deny(f"Ticket is invalid: {exc.reason}")

        return self._grant("Access granted")

    def _check_restricted_access(self) -> bool:
        """Restricted zones: only employees with the right role."""
        position = getattr(self._person, "position", None)
        if position is None:
            return self._deny("Not an employee")

        allowed = AccessControl.RESTRICTED_ROLES.get(self._zone, set())
        if position not in allowed:
            return self._deny(
                f"Role '{position}' is not allowed into zone '{self._zone}'"
            )
        return self._grant("Access granted")

    def _grant(self, reason: str) -> bool:
        self._is_granted = True
        self._reason = reason
        return True

    def _deny(self, reason: str) -> bool:
        self._is_granted = False
        self._reason = reason
        return False


    def log_entry(self) -> dict:
        """Return a dict suitable for a security journal entry."""
        return {
            "person": getattr(self._person, "name", "unknown"),
            "zone": self._zone,
            "time": self._time,
            "granted": self._is_granted,
            "reason": self._reason,
        }