from datetime import date

from exceptions.InvalidCargoStateException import InvalidCargoStateException


class CargoManifest:
    """List of cargo items on a shipment."""

    def __init__(self, shipment, issuer: str):
        if shipment is None:
            raise ValueError("Shipment must not be None")
        if not issuer:
            raise ValueError("Issuer must not be empty")
        self._shipment = shipment
        self._items = []
        self._issuer = issuer
        self._is_verified = False
        self._issued_date = date.today()

    @property
    def shipment(self):
        return self._shipment

    @property
    def items(self):
        return list(self._items)

    @property
    def issuer(self):
        return self._issuer

    @property
    def is_verified(self):
        return self._is_verified

    @property
    def issued_date(self):
        return self._issued_date

    def add_item(self, cargo):
        """Add cargo to the manifest."""
        if cargo is None:
            raise ValueError("Cargo must not be None")
        if self._is_verified:
            raise InvalidCargoStateException(
                title=self._shipment.number,
                state="verified",
                reason="Cannot change a verified manifest",
            )
        self._items.append(cargo)
        return True

    def remove_item(self, cargo):
        """Remove cargo from the manifest."""
        if self._is_verified:
            raise InvalidCargoStateException(
                title=self._shipment.number,
                state="verified",
                reason="Cannot change a verified manifest",
            )
        if cargo not in self._items:
            raise ValueError("Cargo is not on this manifest")
        self._items.remove(cargo)
        return True

    def verify(self):
        """Lock the manifest."""
        if self._is_verified:
            raise InvalidCargoStateException(
                title=self._shipment.number,
                state="verified",
                reason="Manifest is already verified",
            )
        if not self._items:
            raise ValueError("Cannot verify an empty manifest")
        self._is_verified = True
        return True

    def total_weight(self) -> float:
        """Sum of item weights."""
        return sum(item.weight for item in self._items)
