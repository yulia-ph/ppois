from exceptions.CargoOverweightException import CargoOverweightException
from exceptions.InvalidCargoStateException import InvalidCargoStateException


class Pallet:
    """A pallet that holds packages."""

    def __init__(self, code: str, max_weight: float):
        if not code:
            raise ValueError("Code must not be empty")
        if max_weight <= 0:
            raise ValueError(f"Max weight must be positive, got {max_weight}")
        self._code = code
        self._packages = []
        self._max_weight = max_weight
        self._is_wrapped = False

    @property
    def code(self):
        return self._code

    @property
    def packages(self):
        return list(self._packages)

    @property
    def max_weight(self):
        return self._max_weight

    @property
    def is_wrapped(self):
        return self._is_wrapped

    def total_weight(self) -> float:
        """Sum of package content weights."""
        return sum(pkg.contents.weight for pkg in self._packages)

    def add_package(self, package):
        """Put a package on the pallet.

        Raises:
            CargoOverweightException: If the pallet would go over max weight.
        """
        if package is None:
            raise ValueError("Package must not be None")
        if self._is_wrapped:
            raise InvalidCargoStateException(
                title=self._code,
                state="wrapped",
                reason="Cannot add packages to a wrapped pallet",
            )
        if package in self._packages:
            raise ValueError("Package is already on this pallet")
        next_weight = self.total_weight() + package.contents.weight
        if next_weight > self._max_weight:
            raise CargoOverweightException(weight=next_weight, limit=self._max_weight)
        self._packages.append(package)
        return True

    def wrap(self):
        """Wrap the pallet for transport."""
        if self._is_wrapped:
            raise InvalidCargoStateException(
                title=self._code,
                state="wrapped",
                reason="Pallet is already wrapped",
            )
        self._is_wrapped = True
        return True

    def unwrap(self):
        """Remove the wrap."""
        if not self._is_wrapped:
            raise InvalidCargoStateException(
                title=self._code,
                state="open",
                reason="Pallet is not wrapped",
            )
        self._is_wrapped = False
        return True
