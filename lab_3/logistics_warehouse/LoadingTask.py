from datetime import datetime, timedelta

from exceptions.InvalidCargoStateException import InvalidCargoStateException


class LoadingTask:
    """Loading an order at a dock."""

    STATUS_OPEN = "open"
    STATUS_RUNNING = "running"
    STATUS_DONE = "done"

    def __init__(self, dock, order, worker):
        if dock is None or order is None or worker is None:
            raise ValueError("Dock, order and worker must not be None")
        self._dock = dock
        self._order = order
        self._worker = worker
        self._status = LoadingTask.STATUS_OPEN
        self._started_at = None

    @property
    def dock(self):
        return self._dock

    @property
    def order(self):
        return self._order

    @property
    def worker(self):
        return self._worker

    @property
    def status(self):
        return self._status

    @property
    def started_at(self):
        return self._started_at

    def assign_worker(self, worker):
        """Change the worker before the task starts."""
        if worker is None:
            raise ValueError("Worker must not be None")
        if self._status != LoadingTask.STATUS_OPEN:
            raise InvalidCargoStateException(
                title=self._order.number,
                state=self._status,
                reason="Cannot reassign a started task",
            )
        self._worker = worker
        return True

    def start(self):
        """Start loading."""
        if self._status != LoadingTask.STATUS_OPEN:
            raise InvalidCargoStateException(
                title=self._order.number,
                state=self._status,
                reason="Task is not open",
            )
        self._started_at = datetime.now()
        self._status = LoadingTask.STATUS_RUNNING
        return True

    def finish(self):
        """Finish loading."""
        if self._status != LoadingTask.STATUS_RUNNING:
            raise InvalidCargoStateException(
                title=self._order.number,
                state=self._status,
                reason="Task is not running",
            )
        self._status = LoadingTask.STATUS_DONE
        return True

    def is_overdue(self, limit_minutes: int = 60, now: datetime = None) -> bool:
        """True if running longer than `limit_minutes`."""
        if self._started_at is None:
            return False
        moment = now or datetime.now()
        return moment - self._started_at > timedelta(minutes=limit_minutes)
