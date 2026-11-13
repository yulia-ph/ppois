from datetime import datetime

from exceptions.DeliveryRefusedException import DeliveryRefusedException
from exceptions.InvalidCargoStateException import InvalidCargoStateException


class Delivery:
    """Closing a shipment at the consignee."""

    def __init__(self, order):
        if order is None:
            raise ValueError("Order must not be None")
        self._order = order
        self._completed_at = None
        self._signature = None
        self._is_partial = False
        self._notes = []
        self._refused = False

    @property
    def order(self):
        return self._order

    @property
    def completed_at(self):
        return self._completed_at

    @property
    def signature(self):
        return self._signature

    @property
    def is_partial(self):
        return self._is_partial

    @property
    def notes(self):
        return list(self._notes)

    def confirm(self, signature: str):
        """Sign and complete the delivery, and deliver the order."""
        if not signature:
            raise ValueError("Signature must not be empty")
        if self._refused:
            raise InvalidCargoStateException(
                title=self._order.number,
                state="refused",
                reason="Cannot confirm a refused delivery",
            )
        if self._completed_at is not None:
            raise InvalidCargoStateException(
                title=self._order.number,
                state="completed",
                reason="Delivery is already completed",
            )
        self._signature = signature
        self._completed_at = datetime.now()
        if self._order.status == "dispatched":
            self._order.deliver()
        return True

    def mark_partial(self):
        """Mark the delivery as partial."""
        if self._completed_at is not None:
            raise InvalidCargoStateException(
                title=self._order.number,
                state="completed",
                reason="Cannot mark a completed delivery as partial",
            )
        self._is_partial = True
        return True

    def refuse(self, reason: str):
        """Refuse the delivery."""
        if not reason:
            raise ValueError("Reason must not be empty")
        if self._completed_at is not None:
            raise InvalidCargoStateException(
                title=self._order.number,
                state="completed",
                reason="Cannot refuse a completed delivery",
            )
        self._refused = True
        self._notes.append(reason)
        raise DeliveryRefusedException(reason=reason)

    def attach_note(self, note: str):
        """Add a free-form note."""
        if not note:
            raise ValueError("Note must not be empty")
        self._notes.append(note)
        return True
