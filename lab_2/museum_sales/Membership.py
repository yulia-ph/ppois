from datetime import date, timedelta


class Membership:
    """A visitor's museum membership.

    Memberships grant discounts on tickets, shop purchases, and other
    paid services. Each membership has a level (basic/silver/gold) that
    defines its discount rate, and a validity date.

    An expired membership is not an error — it simply returns 0.0
    discount and reports is_active() == False.
    """

    LEVEL_BASIC = "basic"
    LEVEL_SILVER = "silver"
    LEVEL_GOLD = "gold"

    LEVELS = {
        LEVEL_BASIC: 0.10,
        LEVEL_SILVER: 0.20,
        LEVEL_GOLD: 0.50,
    }

    DAYS_PER_MONTH = 30

    def __init__(self, visitor, level: str, valid_until: date):
        """Initialize a membership.

        Args:
            visitor: The member. Must not be None.
            level: One of LEVELS keys.
            valid_until: The last day the membership is valid.

        Raises:
            ValueError: If visitor is None, valid_until is None, or
                level is not a recognized membership level.
        """
        if visitor is None:
            raise ValueError("Visitor must not be None")
        if valid_until is None:
            raise ValueError("Valid-until date must not be None")
        if level not in Membership.LEVELS:
            raise ValueError(
                f"Invalid membership level '{level}'. "
                f"Must be one of {tuple(Membership.LEVELS.keys())}"
            )
        self._visitor = visitor
        self._level = level
        self._valid_until = valid_until


    @property
    def visitor(self):
        return self._visitor

    @property
    def level(self):
        return self._level

    @property
    def valid_until(self):
        return self._valid_until


    def is_active(self, today: date = None) -> bool:
        """Return True if the membership is still valid.

        Args:
            today: Optional date override (defaults to today).
        """
        if today is None:
            today = date.today()
        return today <= self._valid_until

    def check_discount(self) -> float:
        """Return the discount rate for this membership.

        Returns 0.0 if the membership has expired.
        """
        if not self.is_active():
            return 0.0
        return Membership.LEVELS[self._level]


    def renew(self, months: int):
        """Extend the membership by the given number of months.

        If the membership is still active, extends from its current
        end date. If expired, extends from today.

        Args:
            months: Number of months to add. Must be positive.

        Raises:
            ValueError: If months is not positive.
        """
        if months <= 0:
            raise ValueError(f"Months must be positive, got {months}")
        base = max(self._valid_until, date.today())
        self._valid_until = base + timedelta(days=Membership.DAYS_PER_MONTH * months)
        return True
