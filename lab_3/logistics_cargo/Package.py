from exceptions.InvalidCargoStateException import InvalidCargoStateException


class Package:
    """A sealed package wrapping cargo contents."""

    OVERSIZE_M = 1.5

    _counter = 0

    def __init__(self, contents, size: float):
        if contents is None:
            raise ValueError("Contents must not be None")
        if size <= 0:
            raise ValueError(f"Size must be positive, got {size}")
        Package._counter += 1
        self._tracking_number = f"PKG-{Package._counter:06d}"
        self._contents = contents
        self._size = size
        self._is_sealed = False

    @property
    def tracking_number(self):
        return self._tracking_number

    @property
    def contents(self):
        return self._contents

    @property
    def size(self):
        return self._size

    @property
    def is_sealed(self):
        return self._is_sealed

    def seal(self):
        """Seal the package."""
        if self._is_sealed:
            raise InvalidCargoStateException(
                title=self._tracking_number,
                state="sealed",
                reason="Package is already sealed",
            )
        self._is_sealed = True
        return True

    def unseal(self):
        """Open the package."""
        if not self._is_sealed:
            raise InvalidCargoStateException(
                title=self._tracking_number,
                state="open",
                reason="Package is not sealed",
            )
        self._is_sealed = False
        return True

    def scan(self) -> str:
        """Return the tracking number (a scan result)."""
        return self._tracking_number

    def is_oversize(self) -> bool:
        """Return True if the longest side exceeds the oversize limit."""
        return self._size > Package.OVERSIZE_M
