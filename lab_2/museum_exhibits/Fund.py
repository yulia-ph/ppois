from exceptions.InvalidExhibitStateException import InvalidExhibitStateException


class Fund:
    """A museum fund — a large accounting unit above collections.

    A fund groups thematic collections by type (painting, sculpture,
    document) or as mixed. Funds are the unit through which exhibits
    are formally accepted into the museum and written off from it.

    An exhibit is accepted into the fund through its type-matching
    collections; when no matching collection is available, the exhibit
    cannot be accepted.
    """

    TYPE_PAINTING = "painting"
    TYPE_SCULPTURE = "sculpture"
    TYPE_DOCUMENT = "document"
    TYPE_MIXED = "mixed"

    VALID_TYPES = (TYPE_PAINTING, TYPE_SCULPTURE, TYPE_DOCUMENT, TYPE_MIXED)

    CLASS_TO_TYPE = {
        "Painting": TYPE_PAINTING,
        "Sculpture": TYPE_SCULPTURE,
        "Document": TYPE_DOCUMENT,
    }

    def __init__(self, name: str, fund_type: str):
        """Initialize a fund.

        Args:
            name: The fund name. Must not be empty.
            fund_type: One of the TYPE_* constants.

        Raises:
            ValueError: If name is empty or fund_type is not valid.
        """
        if not name:
            raise ValueError("Fund name must not be empty")
        if fund_type not in Fund.VALID_TYPES:
            raise ValueError(
                f"Invalid fund type '{fund_type}'. Must be one of {Fund.VALID_TYPES}"
            )
        self._name = name
        self._type = fund_type
        self._collections = []
        self._written_off = []


    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def collections(self):
        return list(self._collections)

    @property
    def written_off(self):
        return list(self._written_off)


    def add_collection(self, collection):
        """Add a collection to this fund.

        Args:
            collection: The collection to add. Must not be None.

        Raises:
            ValueError: If collection is None or already in the fund.
        """
        if collection is None:
            raise ValueError("Collection must not be None")
        if collection in self._collections:
            raise ValueError(
                f"Collection '{collection.name}' is already in fund '{self._name}'"
            )
        self._collections.append(collection)
        return True

    def remove_collection(self, collection):
        """Remove a collection from this fund.

        Args:
            collection: The collection to remove.

        Raises:
            ValueError: If the collection is not in this fund.
        """
        if collection not in self._collections:
            raise ValueError(
                f"Collection '{collection.name}' is not in fund '{self._name}'"
            )
        self._collections.remove(collection)
        return True

    def find_collection(self, name: str):
        """Find a collection by name.

        Args:
            name: The collection name.

        Returns:
            The matching Collection.

        Raises:
            ValueError: If no collection with the given name exists.
        """
        for collection in self._collections:
            if collection.name == name:
                return collection
        raise ValueError(f"Collection '{name}' not found in fund '{self._name}'")

    def accept_item(self, exhibit):
        """Accept an exhibit into the fund.

        Args:
            exhibit: The exhibit to accept. Must not be None.

        Raises:
            ValueError: If exhibit is None, or its class does not match
                the fund's type.
            InvalidExhibitStateException: If no collection accepted the
                exhibit.
        """
        self._ensure_exhibit_not_none(exhibit)
        self._ensure_type_matches(exhibit)
        self._add_to_first_collection(exhibit)
        return True

    def _ensure_exhibit_not_none(self, exhibit):
        if exhibit is None:
            raise ValueError("Exhibit must not be None")

    def _ensure_type_matches(self, exhibit):
        exhibit_kind = Fund.CLASS_TO_TYPE.get(exhibit.__class__.__name__)
        if self._type != Fund.TYPE_MIXED and self._type != exhibit_kind:
            raise ValueError(
                f"Exhibit of class '{exhibit.__class__.__name__}' "
                f"cannot be accepted into fund of type '{self._type}'"
            )

    def _add_to_first_collection(self, exhibit):
        for collection in self._collections:
            if self._try_add(collection, exhibit):
                return
        raise InvalidExhibitStateException(
            exhibit_title=exhibit.title,
            state="not_accepted",
            reason=f"No collection in fund '{self._name}' accepted the exhibit",
        )

    def _try_add(self, collection, exhibit) -> bool:
        try:
            collection.add_exhibit(exhibit)
            return True
        except (ValueError, InvalidExhibitStateException):
            return False
    def write_off_item(self, exhibit):
        """Write off an exhibit from the fund.

        Removes the exhibit from its collection and adds it to the
        fund's written-off list.

        Args:
            exhibit: The exhibit to write off. Must not be None.

        Raises:
            ValueError: If exhibit is None or not in any collection of
                this fund.
        """
        if exhibit is None:
            raise ValueError("Exhibit must not be None")
        for collection in self._collections:
            if exhibit in collection.exhibits:
                collection.remove_exhibit(exhibit)
                self._written_off.append(exhibit)
                return True
        raise ValueError(
            f"Exhibit '{exhibit.inventory_number}' is not in fund '{self._name}'"
        )


    def count_exhibits(self) -> int:
        """Return the total number of exhibits across all collections."""
        return sum(c.count_exhibits() for c in self._collections)

    def total_value(self) -> float:
        """Return the total insurance value across all collections."""
        return sum(c.calculate_total_value() for c in self._collections)

    def generate_report(self) -> dict:
        """Return a summary dict of the fund's state."""
        return {
            "fund": self._name,
            "type": self._type,
            "collections": len(self._collections),
            "exhibits": self.count_exhibits(),
            "total_value": self.total_value(),
            "written_off": len(self._written_off),
        }

    def needs_restoration(self) -> list:
        """Return all exhibits in the fund that require restoration."""
        result = []
        for collection in self._collections:
            for exhibit in collection.exhibits:
                if exhibit.needs_restoration():
                    result.append(exhibit)
        return result