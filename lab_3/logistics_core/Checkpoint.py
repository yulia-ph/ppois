from exceptions.HazardousRestrictionException import HazardousRestrictionException


class Checkpoint:
    """A road or border checkpoint."""

    def __init__(self, name: str, address, is_border: bool = False):
        """Initialize a checkpoint.

        Raises:
            ValueError: If name is empty or address is None.
        """
        if not name:
            raise ValueError("Checkpoint name must not be empty")
        if address is None:
            raise ValueError("Address must not be None")
        self._name = name
        self._address = address
        self._is_border = is_border
        self._required_documents = []
        self._is_open = True

    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self._address

    @property
    def is_border(self):
        return self._is_border

    @property
    def required_documents(self):
        return list(self._required_documents)

    @property
    def is_open(self):
        return self._is_open

    def require_document(self, document_name: str):
        """Add a required document type.

        Raises:
            ValueError: If document_name is empty or already required.
        """
        if not document_name:
            raise ValueError("Document name must not be empty")
        if document_name in self._required_documents:
            raise ValueError(f"Document '{document_name}' is already required")
        self._required_documents.append(document_name)
        return True

    def inspect(self, cargo):
        """Inspect cargo at this checkpoint.

        Raises:
            ValueError: If cargo is None or the checkpoint is closed.
            HazardousRestrictionException: If hazardous cargo needs a permit.
        """
        if cargo is None:
            raise ValueError("Cargo must not be None")
        if not self._is_open:
            raise ValueError("Checkpoint is closed")
        needs_permit = getattr(cargo, "needs_permit", None)
        if callable(needs_permit) and needs_permit():
            raise HazardousRestrictionException(
                reason="Hazardous cargo requires a permit at this checkpoint",
            )
        return True

    def allow_passage(self, cargo):
        """Allow cargo through after a successful inspect."""
        self.inspect(cargo)
        return True

    def deny_passage(self, reason: str):
        """Refuse passage.

        Raises:
            ValueError: If reason is empty.
            HazardousRestrictionException: Always, with the given reason.
        """
        if not reason:
            raise ValueError("Reason must not be empty")
        raise HazardousRestrictionException(reason=reason)
