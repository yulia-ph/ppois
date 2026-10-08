from exceptions.ExhibitNotFoundException import ExhibitNotFoundException


class Catalog:
    """A searchable catalog of exhibits in a museum.

    Maintains an internal list of exhibits and an index by inventory
    number for fast lookups. Provides search and filter operations
    based on exhibit attributes (title, author, condition, collection).

    The catalog does not own the exhibits — it only references them.
    Removing an exhibit from the catalog does not delete it from the
    museum's collection or storage.
    """

    def __init__(self):
        """Initialize an empty catalog."""
        self._items = []
        self._index = {}  # inventory_number -> Exhibit


    @property
    def items(self):
        return list(self._items)

    @property
    def is_empty(self):
        return len(self._items) == 0


    def add(self, exhibit):
        """Add an exhibit to the catalog.

        Args:
            exhibit: The exhibit to add. Must expose an
                `inventory_number` attribute.

        Raises:
            ValueError: If exhibit is None, or an exhibit with the same
                inventory number is already in the catalog.
        """
        if exhibit is None:
            raise ValueError("Exhibit must not be None")
        if exhibit.inventory_number in self._index:
            raise ValueError(
                f"Exhibit '{exhibit.inventory_number}' is already in the catalog"
            )
        self._items.append(exhibit)
        self._index[exhibit.inventory_number] = exhibit
        return True

    def remove(self, exhibit):
        """Remove an exhibit from the catalog.

        Args:
            exhibit: The exhibit to remove.

        Raises:
            ValueError: If exhibit is None, or the exhibit is not in
                the catalog.
        """
        if exhibit is None:
            raise ValueError("Exhibit must not be None")
        if exhibit.inventory_number not in self._index:
            raise ValueError(
                f"Exhibit '{exhibit.inventory_number}' is not in the catalog"
            )
        self._items.remove(exhibit)
        del self._index[exhibit.inventory_number]
        return True

    def find_by_number(self, inventory_number: str):
        """Find an exhibit by its inventory number.

        Args:
            inventory_number: The inventory number to look up.

        Returns:
            The matching Exhibit.

        Raises:
            ExhibitNotFoundException: If no exhibit with the given
                number exists in the catalog.
        """
        exhibit = self._index.get(inventory_number)
        if exhibit is None:
            raise ExhibitNotFoundException(inventory_number)
        return exhibit


    def search(self, query: str) -> list:
        """Search exhibits by title or author (case-insensitive substring).

        Args:
            query: The search string. Must not be empty.

        Returns:
            A list of exhibits whose title or author contains the query.

        Raises:
            ValueError: If query is empty or None.
        """
        if not query:
            raise ValueError("Search query must not be empty")
        q = query.lower()
        return [
            ex for ex in self._items
            if q in ex.title.lower() or q in ex.author.lower()
        ]

    def filter_by_condition(self, condition: str) -> list:
        """Return exhibits whose condition matches exactly.

        Args:
            condition: One of the exhibit condition constants
                (e.g. "excellent", "good", "damaged", "critical").
        """
        return [ex for ex in self._items if ex.condition == condition]

    def filter_by_collection(self, collection) -> list:
        """Return exhibits that belong to the given collection."""
        return [ex for ex in self._items if ex.collection == collection]

    def filter_by_author(self, author: str) -> list:
        """Return exhibits by the given author (exact match)."""
        return [ex for ex in self._items if ex.author == author]

    def filter_by_class(self, class_name: str) -> list:
        """Return exhibits whose class name matches.

        Args:
            class_name: The class name to filter by, e.g. "Painting",
                "Sculpture", "Document".
        """
        return [ex for ex in self._items if ex.__class__.__name__ == class_name]


    def count(self) -> int:
        """Return the number of exhibits in the catalog."""
        return len(self._items)

    def total_value(self) -> float:
        """Return the total insurance value of all exhibits in the catalog."""
        return sum(ex.insurance_value for ex in self._items)

    def by_condition_stats(self) -> dict:
        """Return a dict mapping each condition to the number of exhibits.

        Example:
            {"good": 5, "damaged": 2, "critical": 1}
        """
        stats = {}
        for ex in self._items:
            stats[ex.condition] = stats.get(ex.condition, 0) + 1
        return stats

