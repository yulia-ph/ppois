from exceptions.InvalidCargoStateException import InvalidCargoStateException


class StockMove:
    """Moving cargo from one zone to another."""

    def __init__(self, cargo, from_zone, to_zone, worker):
        if cargo is None or from_zone is None or to_zone is None or worker is None:
            raise ValueError("Cargo, zones and worker must not be None")
        if from_zone is to_zone:
            raise ValueError("From and to zones must differ")
        self._cargo = cargo
        self._from_zone = from_zone
        self._to_zone = to_zone
        self._worker = worker
        self._is_confirmed = False
        self._registered = False

    @property
    def cargo(self):
        return self._cargo

    @property
    def from_zone(self):
        return self._from_zone

    @property
    def to_zone(self):
        return self._to_zone

    @property
    def worker(self):
        return self._worker

    @property
    def is_confirmed(self):
        return self._is_confirmed

    def register(self):
        """Register the move before confirming it."""
        if self._registered:
            raise InvalidCargoStateException(
                title=self._cargo.tracking_id,
                state="registered",
                reason="Move is already registered",
            )
        self._registered = True
        return True

    def confirm(self):
        """Confirm a registered move."""
        if not self._registered:
            raise InvalidCargoStateException(
                title=self._cargo.tracking_id,
                state="draft",
                reason="Register the move first",
            )
        if self._is_confirmed:
            raise InvalidCargoStateException(
                title=self._cargo.tracking_id,
                state="confirmed",
                reason="Move is already confirmed",
            )
        self._is_confirmed = True
        return True

    def cancel(self):
        """Cancel a move that is not yet confirmed."""
        if self._is_confirmed:
            raise InvalidCargoStateException(
                title=self._cargo.tracking_id,
                state="confirmed",
                reason="Cannot cancel a confirmed move",
            )
        self._registered = False
        return True
