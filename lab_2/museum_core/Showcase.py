from exceptions.AccessDeniedException import AccessDeniedException
from exceptions.InvalidExhibitStateException import InvalidExhibitStateException
from museum_exhibits.Exhibit import Exhibit


class Showcase:
    """A physical display case inside a hall.

    A showcase holds at most one exhibit. It has a locking mechanism
    that can only be operated by museum staff, and it can report
    whether the exhibit inside needs restoration.

    The showcase does not own the exhibit — it only references it.
    """

    DAMAGED_CONDITIONS = (Exhibit.CONDITION_DAMAGED, Exhibit.CONDITION_CRITICAL)
    STUB_HUMIDITY_VALUE = 0.0

    def __init__(self, inventory_number: str, showcase_type: str):
        """Initialize a showcase.

        Args:
            inventory_number: A unique inventory number for the showcase.
            showcase_type: A free-form type label (e.g. "horizontal",
                "vertical", "wall-mounted").

        Raises:
            ValueError: If inventory_number is empty.
            TypeError: If showcase_type is not a string.
        """
        if not inventory_number:
            raise ValueError("Showcase inventory number must not be empty")
        if not isinstance(showcase_type, str):
            raise TypeError(
                f"showcase_type must be a string, got {type(showcase_type).__name__}"
            )
        self._inventory_number = inventory_number
        self._type = showcase_type
        self._exhibit = None
        self._is_locked = True


    @property
    def inventory_number(self):
        return self._inventory_number

    @property
    def type(self):
        return self._type

    @property
    def exhibit(self):
        return self._exhibit

    @property
    def is_locked(self):
        return self._is_locked

    @property
    def is_empty(self):
        return self._exhibit is None


    def open_showcase(self, employee):
        """Unlock the showcase for an authorized employee.

        The employee must expose a `position` attribute (typically an
        Employee subclass instance). Visitors and anonymous objects
        are not allowed to open showcases.

        Args:
            employee: The staff member opening the showcase.

        Raises:
            AccessDeniedException: If the employee has no `position`
                attribute.
            InvalidExhibitStateException: If the showcase is already open.
        """
        if not self._is_locked:
            raise InvalidExhibitStateException(
                exhibit_title=self._inventory_number,
                state="open",
                reason="Showcase is already open",
            )
        if not hasattr(employee, "position"):
            raise AccessDeniedException(
                person_name=getattr(employee, "name", "unknown"),
                zone=f"showcase:{self._inventory_number}",
            )
        self._is_locked = False
        return True

    def close_showcase(self):
        """Lock the showcase.

        Idempotent: calling on an already closed showcase is not an error.
        """
        self._is_locked = True
        return True


    def place_exhibit(self, exhibit: Exhibit):
        """Place an exhibit into this showcase.

        The showcase must be empty.

        Args:
            exhibit: The exhibit to display. Must not be None.

        Raises:
            ValueError: If exhibit is None.
            InvalidExhibitStateException: If the showcase already holds
                an exhibit.
        """
        if exhibit is None:
            raise ValueError("Exhibit must not be None")
        if not self.is_empty:
            raise InvalidExhibitStateException(
                exhibit_title=self._exhibit.title,
                state=self._exhibit.condition,
                reason=f"Showcase '{self._inventory_number}' is already occupied",
            )
        self._exhibit = exhibit
        return True

    def remove_exhibit(self) -> Exhibit:
        """Remove and return the exhibit currently in the showcase.

        Returns:
            The exhibit that was removed.

        Raises:
            InvalidExhibitStateException: If the showcase is empty.
        """
        if self.is_empty:
            raise InvalidExhibitStateException(
                exhibit_title=None,
                state="empty",
                reason=f"Showcase '{self._inventory_number}' is empty",
            )
        old = self._exhibit
        self._exhibit = None
        return old


    def check_humidity(self) -> float:
        """Return the current humidity inside the showcase.

        Stub: always returns 0.0. Real implementation would read from
        an attached humidity sensor.
        """
        return Showcase.STUB_HUMIDITY_VALUE

    def needs_restoration(self) -> bool:
        """Return True if the exhibit inside is damaged or critical.

        Returns False when the showcase is empty.
        """
        if self._exhibit is None:
            return False
        return self._exhibit.condition in Showcase.DAMAGED_CONDITIONS