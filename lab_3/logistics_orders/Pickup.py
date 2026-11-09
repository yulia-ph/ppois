from datetime import datetime

from exceptions.InvalidCargoStateException import InvalidCargoStateException


class Pickup:
    """Collecting cargo at a warehouse."""

    STATUS_PLANNED = "planned"
    STATUS_DONE = "done"
    STATUS_FAILED = "failed"

    def __init__(self, order, warehouse, window_start: datetime, window_end: datetime):
        if order is None or warehouse is None:
            raise ValueError("Order and warehouse must not be None")
        if window_start is None or window_end is None:
            raise ValueError("Window bounds must not be None")
        if window_end <= window_start:
            raise ValueError("Window end must be after start")
        self._order = order
        self._warehouse = warehouse
        self._window_start = window_start
        self._window_end = window_end
        self._status = Pickup.STATUS_PLANNED

    @property
    def order(self):
        return self._order

    @property
    def warehouse(self):
        return self._warehouse

    @property
    def window_start(self):
        return self._window_start

    @property
    def window_end(self):
        return self._window_end

    @property
    def status(self):
        return self._status

    def schedule(self, window_start: datetime, window_end: datetime):
        """Set the first pickup window (alias for construction-time planning)."""
        return self.reschedule(window_start, window_end)

    def reschedule(self, window_start: datetime, window_end: datetime):
        """Move the pickup window."""
        if self._status != Pickup.STATUS_PLANNED:
            raise InvalidCargoStateException(
                title=self._order.number,
                state=self._status,
                reason="Cannot reschedule a finished pickup",
            )
        if window_end <= window_start:
            raise ValueError("Window end must be after start")
        self._window_start = window_start
        self._window_end = window_end
        return True

    def complete(self):
        """Finish the pickup and ship cargo from the warehouse if present."""
        if self._status != Pickup.STATUS_PLANNED:
            raise InvalidCargoStateException(
                title=self._order.number,
                state=self._status,
                reason="Pickup is not planned",
            )
        cargo = self._order.cargo
        stored = self._warehouse.find_cargo()
        if cargo in stored:
            self._warehouse.ship(cargo)
        self._status = Pickup.STATUS_DONE
        return True

    def fail(self, reason: str):
        """Mark the pickup as failed."""
        if not reason:
            raise ValueError("Reason must not be empty")
        if self._status != Pickup.STATUS_PLANNED:
            raise InvalidCargoStateException(
                title=self._order.number,
                state=self._status,
                reason="Pickup is not planned",
            )
        self._status = Pickup.STATUS_FAILED
        return True
