from datetime import date

from exceptions.InvalidExhibitStateException import InvalidExhibitStateException


class StorageMoveAct:
    """An act of moving an exhibit between storages.

    The act must be confirmed before the movement can be registered.
    Registering the movement:

        1. Removes the exhibit from the source storage.
        2. Adds it to the destination storage.
        3. Updates the exhibit's location.

    If step 2 fails, step 1 is rolled back.
    """

    def __init__(self, exhibit, from_storage, to_storage, responsible):
        """Initialize a storage move act.

        Args:
            exhibit: The exhibit being moved. Must not be None.
            from_storage: Source storage. Must not be None.
            to_storage: Destination storage. Must not be None and must
                differ from from_storage.
            responsible: Employee responsible for the move. Must not
                be None.

        Raises:
            ValueError: If any argument is None, or the storages are
                the same.
        """
        if exhibit is None:
            raise ValueError("Exhibit must not be None")
        if from_storage is None:
            raise ValueError("Source storage must not be None")
        if to_storage is None:
            raise ValueError("Destination storage must not be None")
        if from_storage is to_storage:
            raise ValueError("Source and destination storages must differ")
        if responsible is None:
            raise ValueError("Responsible employee must not be None")

        self._exhibit = exhibit
        self._from_storage = from_storage
        self._to_storage = to_storage
        self._responsible = responsible
        self._date = date.today()
        self._is_confirmed = False


    @property
    def exhibit(self):
        return self._exhibit

    @property
    def from_storage(self):
        return self._from_storage

    @property
    def to_storage(self):
        return self._to_storage

    @property
    def responsible(self):
        return self._responsible

    @property
    def date(self):
        return self._date

    @property
    def is_confirmed(self):
        return self._is_confirmed


    def create(self):
        """Validate the act before confirmation.

        Returns True if the act is well-formed.

        Raises:
            InvalidExhibitStateException: If any required element is
                missing or invalid.
        """
        if not self._from_storage.has_exhibit(self._exhibit):
            raise InvalidExhibitStateException(
                exhibit_title=self._exhibit.inventory_number,
                state="not_in_source",
                reason=f"Exhibit is not in source storage '{self._from_storage.name}'",
            )
        return True

    def confirm(self):
        """Confirm the act, allowing the movement to be registered.

        Idempotent: confirming an already confirmed act is not an error.

        Raises:
            InvalidExhibitStateException: Propagated from create().
        """
        if self._is_confirmed:
            return True
        self.create()
        self._is_confirmed = True
        return True

    def register_movement(self):
        """Execute the movement: remove from source, add to destination.

        Raises:
            InvalidExhibitStateException: If the act is not confirmed,
                or the source/destination storages reject the move.
        """
        if not self._is_confirmed:
            raise InvalidExhibitStateException(
                exhibit_title=self._exhibit.inventory_number,
                state="not_confirmed",
                reason="Cannot register movement before the act is confirmed",
            )
        self._from_storage.remove_exhibit(self._exhibit)
        try:
            self._to_storage.place_exhibit(self._exhibit)
        except InvalidExhibitStateException:
            self._from_storage.place_exhibit(self._exhibit)
            raise
        self._exhibit.move_to(self._to_storage)
        return True

    def cancel(self):
        """Cancel the act.

        Idempotent: cancelling an already unconfirmed act is not an error.
        """
        self._is_confirmed = False
        return True