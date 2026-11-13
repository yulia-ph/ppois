from exceptions.InvalidCargoStateException import InvalidCargoStateException


class Claim:
    """A damage or delay claim against a shipment."""

    STATUS_FILED = "filed"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"

    def __init__(self, order, reason: str, amount: float):
        if order is None:
            raise ValueError("Order must not be None")
        if not reason:
            raise ValueError("Reason must not be empty")
        if amount <= 0:
            raise ValueError(f"Amount must be positive, got {amount}")
        self._order = order
        self._reason = reason
        self._amount = amount
        self._status = None
        self._evidence = []

    @property
    def order(self):
        return self._order

    @property
    def reason(self):
        return self._reason

    @property
    def amount(self):
        return self._amount

    @property
    def status(self):
        return self._status

    @property
    def evidence(self):
        return list(self._evidence)

    def file(self):
        """File the claim."""
        if self._status is not None:
            raise InvalidCargoStateException(
                title=self._order.number,
                state=self._status,
                reason="Claim is already filed",
            )
        self._status = Claim.STATUS_FILED
        return True

    def add_evidence(self, note: str):
        """Add evidence while the claim is filed."""
        if not note:
            raise ValueError("Evidence must not be empty")
        if self._status != Claim.STATUS_FILED:
            raise InvalidCargoStateException(
                title=self._order.number,
                state=str(self._status),
                reason="Can only add evidence to a filed claim",
            )
        self._evidence.append(note)
        return True

    def approve(self):
        """Approve a filed claim."""
        if self._status != Claim.STATUS_FILED:
            raise InvalidCargoStateException(
                title=self._order.number,
                state=str(self._status),
                reason="Only a filed claim can be approved",
            )
        self._status = Claim.STATUS_APPROVED
        return True

    def reject(self):
        """Reject a filed claim."""
        if self._status != Claim.STATUS_FILED:
            raise InvalidCargoStateException(
                title=self._order.number,
                state=str(self._status),
                reason="Only a filed claim can be rejected",
            )
        self._status = Claim.STATUS_REJECTED
        return True
