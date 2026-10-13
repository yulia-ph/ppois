from datetime import date, timedelta

from museum_exhibitions.Exhibition import Exhibition


class PermanentExhibition(Exhibition):
    """A long-running permanent exhibition.

    Permanent exhibitions do not have a fixed end date — they run
    "indefinitely" (modeled here as start_date + 10 years). Their
    content is expected to rotate periodically; the exhibition tracks
    the last rotation date and the rotation period.

    The curator can update the description at any time, and rotate
    exhibits once the rotation period has elapsed.
    """

    DEFAULT_ROTATION_DAYS = 180
    INDEFINITE_YEARS = 10
    DAYS_PER_YEAR = 365

    def __init__(self, title, start_date, curator, description: str = ""):
        """Initialize a permanent exhibition.

        Args:
            title: The exhibition title.
            start_date: Start date.
            curator: The curator.
            description: Optional initial description.

        Raises:
            ValueError: If inherited validation fails.
        """
        indefinite_days = PermanentExhibition.DAYS_PER_YEAR * PermanentExhibition.INDEFINITE_YEARS
        far_future = start_date + timedelta(days=indefinite_days)
        super().__init__(title, start_date, far_future, curator,
                         type_=Exhibition.TYPE_PERMANENT)
        self._description = description
        self._last_update = start_date
        self._rotation_period_days = PermanentExhibition.DEFAULT_ROTATION_DAYS


    @property
    def description(self):
        return self._description

    @property
    def last_update(self):
        return self._last_update

    @property
    def rotation_period_days(self):
        return self._rotation_period_days


    def update_description(self, new_text: str):
        """Replace the exhibition description.

        Args:
            new_text: The new description. Must not be empty.

        Raises:
            ValueError: If new_text is empty.
        """
        if not new_text:
            raise ValueError("Description must not be empty")
        self._description = new_text
        self._last_update = date.today()
        return True


    def set_rotation_period(self, days: int):
        """Set the number of days between rotations.

        Args:
            days: Period in days. Must be positive.

        Raises:
            ValueError: If days is not positive.
        """
        if days <= 0:
            raise ValueError(f"Rotation period must be positive, got {days}")
        self._rotation_period_days = days
        return True

    def needs_rotation(self, today=None) -> bool:
        """Return True if enough time has passed since the last rotation."""
        if today is None:
            today = date.today()
        delta = (today - self._last_update).days
        return delta >= self._rotation_period_days

    def rotate_exhibits(self, new_exhibits, today=None):
        """Replace current exhibits with a new set.

        Removes all current exhibits (the ones already added via
        add_exhibit), then adds the new ones. Updates last_update.

        Args:
            new_exhibits: Iterable of new exhibits. Must not be empty.
            today: Optional date override.

        Raises:
            ValueError: If new_exhibits is empty.
        """
        if not new_exhibits:
            raise ValueError("New exhibits list must not be empty")
        if today is None:
            today = date.today()
        for ex in list(self._exhibits):
            self.remove_exhibit(ex)
        for ex in new_exhibits:
            self.add_exhibit(ex)
        self._last_update = today
        return True

    def rotate_if_needed(self, new_exhibits, today=None) -> bool:
        """Rotate exhibits only if the rotation period has elapsed.

        Returns:
            True if rotation happened, False if not needed.
        """
        if today is None:
            today = date.today()
        if not self.needs_rotation(today):
            return False
        return self.rotate_exhibits(new_exhibits, today)