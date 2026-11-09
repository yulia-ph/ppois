from exceptions.InvalidCargoStateException import InvalidCargoStateException
from exceptions.VehicleOverloadException import VehicleOverloadException


class Container:
    """An ISO container that holds pallets."""

    def __init__(self, iso_code: str, max_payload: float):
        if not iso_code:
            raise ValueError("ISO code must not be empty")
        if max_payload <= 0:
            raise ValueError(f"Max payload must be positive, got {max_payload}")
        self._iso_code = iso_code
        self._pallets = []
        self._seal_number = None
        self._is_sealed = False
        self._max_payload = max_payload

    @property
    def iso_code(self):
        return self._iso_code

    @property
    def pallets(self):
        return list(self._pallets)

    @property
    def seal_number(self):
        return self._seal_number

    @property
    def is_sealed(self):
        return self._is_sealed

    @property
    def max_payload(self):
        return self._max_payload

    def load_pallet(self, pallet):
        """Load a pallet.

        Raises:
            VehicleOverloadException: If payload would be exceeded.
        """
        if pallet is None:
            raise ValueError("Pallet must not be None")
        if self._is_sealed:
            raise InvalidCargoStateException(
                title=self._iso_code,
                state="sealed",
                reason="Cannot load a sealed container",
            )
        total = sum(p.total_weight() for p in self._pallets) + pallet.total_weight()
        if total > self._max_payload:
            raise VehicleOverloadException(
                plate=self._iso_code,
                weight=total,
                capacity=self._max_payload,
            )
        self._pallets.append(pallet)
        return True

    def unload_pallet(self, pallet):
        """Remove a pallet."""
        if self._is_sealed:
            raise InvalidCargoStateException(
                title=self._iso_code,
                state="sealed",
                reason="Unseal the container first",
            )
        if pallet not in self._pallets:
            raise ValueError("Pallet is not in this container")
        self._pallets.remove(pallet)
        return True

    def seal(self, seal_number: str):
        """Seal the container."""
        if not seal_number:
            raise ValueError("Seal number must not be empty")
        if self._is_sealed:
            raise InvalidCargoStateException(
                title=self._iso_code,
                state="sealed",
                reason="Container is already sealed",
            )
        self._seal_number = seal_number
        self._is_sealed = True
        return True

    def inspect(self) -> bool:
        """Return True if the seal is present and pallets are wrapped."""
        if not self._is_sealed:
            return False
        return all(p.is_wrapped for p in self._pallets)
