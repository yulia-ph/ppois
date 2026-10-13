from exceptions.InvalidExhibitStateException import InvalidExhibitStateException


class Exhibit:
    """Base class for all museum exhibits.

    An exhibit is the central entity of the museum domain: paintings,
    sculptures, and documents are all exhibits. Every exhibit has a
    unique inventory number, a condition, and optional links to a
    collection, an insurance policy, and a physical location
    (storage or showcase).

    Subclasses (Painting, Sculpture, Document) add type-specific
    attributes on top of this base.
    """

    CONDITION_EXCELLENT = "excellent"
    CONDITION_GOOD = "good"
    CONDITION_DAMAGED = "damaged"
    CONDITION_CRITICAL = "critical"

    VALID_CONDITIONS = (
        CONDITION_EXCELLENT,
        CONDITION_GOOD,
        CONDITION_DAMAGED,
        CONDITION_CRITICAL,
    )

    DEFAULT_BASE_PRICE = 1000.0
    CONDITION_MULTIPLIERS = {
        CONDITION_EXCELLENT: 1.5,
        CONDITION_GOOD: 1.0,
        CONDITION_DAMAGED: 0.5,
        CONDITION_CRITICAL: 0.2,
    }
    FALLBACK_MULTIPLIER = 1.0

    _counter = 0

    def __init__(self, title: str, author: str, condition: str = "good"):
        """Initialize an exhibit.

        Args:
            title: The exhibit title. Must not be empty.
            author: The author or creator. Must not be empty.
            condition: One of the CONDITION_* constants.

        Raises:
            ValueError: If title or author is empty, or condition is
                not one of the CONDITION_* constants.
        """
        if not title:
            raise ValueError("Exhibit title must not be empty")
        if not author:
            raise ValueError("Exhibit author must not be empty")
        if condition not in Exhibit.VALID_CONDITIONS:
            raise ValueError(
                f"Invalid condition '{condition}'. "
                f"Must be one of {Exhibit.VALID_CONDITIONS}"
            )

        Exhibit._counter += 1
        self._inventory_number = f"EX-{Exhibit._counter:06d}"
        self._title = title
        self._author = author
        self._condition = condition
        self._collection = None
        self._insurance_value = 0.0
        self._insurance_policy = None
        self._location = None
        self._acquired_date = None


    @property
    def inventory_number(self):
        return self._inventory_number

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @property
    def condition(self):
        return self._condition

    @property
    def collection(self):
        return self._collection

    @property
    def insurance_value(self):
        return self._insurance_value

    @property
    def insurance_policy(self):
        return self._insurance_policy

    @property
    def location(self):
        return self._location

    @property
    def acquired_date(self):
        return self._acquired_date


    def move_to(self, location):
        """Move the exhibit to a physical location.

        Idempotent: moving to the location it already occupies is not
        an error. The exhibit's previous location is not notified —
        location owners (Storage, Showcase) manage their own contents.

        Args:
            location: A Storage or Showcase instance. Must not be None.

        Raises:
            ValueError: If location is None.
        """
        if location is None:
            raise ValueError("Location must not be None")
        self._location = location
        return True

    def remove_from_location(self):
        """Detach the exhibit from its current location.

        Idempotent: calling when the exhibit has no location is not
        an error.
        """
        self._location = None
        return True


    def attach_to_collection(self, collection):
        """Attach the exhibit to a collection.

        Idempotent when called with the same collection it is already
        attached to.

        Args:
            collection: The collection to attach to. Must not be None.

        Raises:
            ValueError: If collection is None.
            InvalidExhibitStateException: If the exhibit is already
                attached to a different collection.
        """
        if collection is None:
            raise ValueError("Collection must not be None")
        if self._collection is collection:
            return True
        if self._collection is not None:
            raise InvalidExhibitStateException(
                exhibit_title=self._title,
                state="in_other_collection",
                reason="Exhibit is already attached to another collection",
            )
        self._collection = collection
        return True

    def remove_from_collection(self):
        """Detach the exhibit from its current collection.

        Idempotent: calling when the exhibit is not in a collection
        is not an error.
        """
        self._collection = None
        return True


    def update_condition(self, new_condition: str):
        """Update the exhibit's condition.

        Args:
            new_condition: One of the CONDITION_* constants.

        Raises:
            ValueError: If new_condition is not a valid condition.
        """
        if new_condition not in Exhibit.VALID_CONDITIONS:
            raise ValueError(
                f"Invalid condition '{new_condition}'. "
                f"Must be one of {Exhibit.VALID_CONDITIONS}"
            )
        self._condition = new_condition
        return True

    def needs_restoration(self) -> bool:
        """Return True if the exhibit is damaged or critical."""
        return self._condition in (
            Exhibit.CONDITION_DAMAGED,
            Exhibit.CONDITION_CRITICAL,
        )

    def is_available_for_exhibition(self) -> bool:
        """Return True if the exhibit can be displayed.

        Critical-condition exhibits cannot be exhibited.
        """
        return self._condition != Exhibit.CONDITION_CRITICAL


    def set_insurance_value(self, value: float):
        """Set the exhibit's insurance value.

        Args:
            value: The insurance value. Must be non-negative.

        Raises:
            ValueError: If value is negative.
        """
        if value < 0:
            raise ValueError(f"Insurance value must be non-negative, got {value}")
        self._insurance_value = value
        return True

    def evaluate_insurance(self, base_price: float = 1000.0) -> float:
        """Re-evaluate the insurance value from condition and base price.

        Multipliers by condition:
            EXCELLENT -> 1.5
            GOOD      -> 1.0
            DAMAGED   -> 0.5
            CRITICAL  -> 0.2

        Args:
            base_price: Base price in conventional units.

        Returns:
            The new insurance value.
        """
        if base_price is None:
            base_price = Exhibit.DEFAULT_BASE_PRICE
        multiplier = Exhibit.CONDITION_MULTIPLIERS.get(
            self._condition, Exhibit.FALLBACK_MULTIPLIER
        )
        self._insurance_value = base_price * multiplier
        return self._insurance_value

    def attach_insurance_policy(self, policy):
        """Attach an insurance policy to the exhibit.

        Args:
            policy: The insurance policy. Must not be None.

        Raises:
            ValueError: If policy is None.
        """
        if policy is None:
            raise ValueError("Insurance policy must not be None")
        self._insurance_policy = policy
        return True


    def send_to_restoration(self, restorer):
        """Send the exhibit to a restorer, creating a Restoration.

        Args:
            restorer: The restorer handling the work. Must not be None.

        Returns:
            The newly created and started Restoration.

        Raises:
            ValueError: If restorer is None.
        """
        if restorer is None:
            raise ValueError("Restorer must not be None")
        from museum_documents.Restoration import Restoration
        restoration = Restoration(self, restorer)
        restoration.start_restoration()
        return restoration


    def set_acquired_date(self, date_):
        """Record the date the exhibit was acquired.

        Args:
            date_: The acquisition date. Must not be None.

        Raises:
            ValueError: If date_ is None.
        """
        if date_ is None:
            raise ValueError("Acquired date must not be None")
        self._acquired_date = date_
        return True


    def __repr__(self):
        return f"<{self.__class__.__name__} {self._inventory_number}: {self._title}>"