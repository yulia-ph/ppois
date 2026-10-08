from exceptions.ExhibitNotFoundException import ExhibitNotFoundException
from exceptions.InvalidExhibitStateException import InvalidExhibitStateException


class Collection:
    """A thematic collection of exhibits.

    A collection groups exhibits by subject, period, or origin (for
    example, "Dutch painting of the 17th century"). A collection is
    curated by a single curator and holds references to its exhibits.

    An exhibit may belong to at most one collection at a time.
    """

    def __init__(self, name: str, theme: str):
        """Initialize a collection.

        Args:
            name: The collection name.
            theme: The thematic focus.

        Raises:
            ValueError: If name or theme is empty.
        """
        if not name:
            raise ValueError("Collection name must not be empty")
        if not theme:
            raise ValueError("Collection theme must not be empty")
        self._name = name
        self._theme = theme
        self._curator = None
        self._exhibits = []


    @property
    def name(self):
        return self._name

    @property
    def theme(self):
        return self._theme

    @property
    def curator(self):
        return self._curator

    @property
    def exhibits(self):
        return list(self._exhibits)

    @property
    def is_empty(self):
        return len(self._exhibits) == 0


    def set_curator(self, curator):
        """Assign a curator to this collection.

        Args:
            curator: The curator to assign. Must not be None.

        Raises:
            ValueError: If curator is None.
        """
        if curator is None:
            raise ValueError("Curator must not be None")
        self._curator = curator
        return True

    def remove_curator(self):
        """Detach the current curator from this collection.

        Idempotent: calling on a collection without a curator is not
        an error.
        """
        self._curator = None
        return True


    def add_exhibit(self, exhibit):
        """Add an exhibit to this collection.

        The exhibit is also notified via `attach_to_collection`, which
        links it back to this collection.

        Args:
            exhibit: The exhibit to add. Must not be None.

        Raises:
            ValueError: If exhibit is None or already in this collection.
            InvalidExhibitStateException: If the exhibit already belongs
                to another collection.
        """
        if exhibit is None:
            raise ValueError("Exhibit must not be None")
        if exhibit in self._exhibits:
            raise ValueError(
                f"Exhibit '{exhibit.inventory_number}' is already in collection '{self._name}'"
            )
        if not exhibit.attach_to_collection(self):
            raise InvalidExhibitStateException(
                exhibit_title=exhibit.title,
                state="in_other_collection",
                reason="Exhibit is already in another collection",
            )
        self._exhibits.append(exhibit)
        return True

    def remove_exhibit(self, exhibit):
        """Remove an exhibit from this collection.

        The exhibit is notified via `remove_from_collection`.

        Args:
            exhibit: The exhibit to remove.

        Raises:
            ValueError: If the exhibit is not in this collection.
        """
        if exhibit not in self._exhibits:
            raise ValueError(
                f"Exhibit '{exhibit.inventory_number}' is not in collection '{self._name}'"
            )
        self._exhibits.remove(exhibit)
        exhibit.remove_from_collection()
        return True

    def find_exhibit(self, inventory_number: str):
        """Find an exhibit in this collection by its inventory number.

        Args:
            inventory_number: The exhibit inventory number.

        Returns:
            The matching Exhibit.

        Raises:
            ExhibitNotFoundException: If no exhibit with the given
                number is in this collection.
        """
        for exhibit in self._exhibits:
            if exhibit.inventory_number == inventory_number:
                return exhibit
        raise ExhibitNotFoundException(inventory_number)

    def count_exhibits(self) -> int:
        """Return the number of exhibits in this collection."""
        return len(self._exhibits)

    def calculate_total_value(self) -> float:
        """Return the total insurance value of all exhibits."""
        return sum(ex.insurance_value for ex in self._exhibits)

    def available_for_exhibition(self) -> list:
        """Return exhibits that can currently be displayed."""
        return [ex for ex in self._exhibits if ex.is_available_for_exhibition()]