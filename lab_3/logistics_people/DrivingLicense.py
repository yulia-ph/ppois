from datetime import date, timedelta

from exceptions.InvalidLicenseException import InvalidLicenseException


class DrivingLicense:
    """A driving license with categories."""

    def __init__(self, number: str, categories, issued_on: date, expires_at: date):
        if not number:
            raise ValueError("License number must not be empty")
        cats = list(categories) if categories else []
        if not cats:
            raise ValueError("License must have at least one category")
        if issued_on is None or expires_at is None:
            raise ValueError("Issued and expiry dates must not be None")
        if expires_at <= issued_on:
            raise ValueError("Expiry must be after issued date")
        self._number = number
        self._categories = cats
        self._issued_on = issued_on
        self._expires_at = expires_at
        self._is_suspended = False

    @property
    def number(self):
        return self._number

    @property
    def categories(self):
        return list(self._categories)

    @property
    def issued_on(self):
        return self._issued_on

    @property
    def expires_at(self):
        return self._expires_at

    @property
    def is_suspended(self):
        return self._is_suspended

    def is_expired(self, on_date: date = None) -> bool:
        """Return True if the license has expired."""
        day = on_date or date.today()
        return day > self._expires_at

    def covers_category(self, category: str) -> bool:
        """Return True if this license covers `category`.

        Raises:
            InvalidLicenseException: If suspended, expired, or category missing.
        """
        if not category:
            raise ValueError("Category must not be empty")
        if self._is_suspended:
            raise InvalidLicenseException(number=self._number, reason="suspended")
        if self.is_expired():
            raise InvalidLicenseException(number=self._number, reason="expired")
        if category not in self._categories:
            raise InvalidLicenseException(
                number=self._number,
                reason=f"missing category {category}",
            )
        return True

    def renew(self, extra_days: int):
        """Extend the expiry date."""
        if extra_days <= 0:
            raise ValueError(f"Extra days must be positive, got {extra_days}")
        if self._is_suspended:
            raise InvalidLicenseException(number=self._number, reason="suspended")
        self._expires_at = self._expires_at + timedelta(days=extra_days)
        return True

    def suspend(self):
        """Suspend the license."""
        self._is_suspended = True
        return True
