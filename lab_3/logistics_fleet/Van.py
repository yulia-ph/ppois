from exceptions.InvalidCargoStateException import InvalidCargoStateException
from logistics_fleet.Vehicle import Vehicle


class Van(Vehicle):
    """A city van with cargo doors."""

    LICENSE_CATEGORY = "B"

    def __init__(
        self,
        plate: str,
        vin: str,
        capacity_kg: float,
        volume_m3: float,
        door_count: int,
        has_liftgate: bool = False,
    ):
        super().__init__(plate, vin, capacity_kg, volume_m3)
        if door_count < 1:
            raise ValueError(f"Door count must be at least 1, got {door_count}")
        self._door_count = door_count
        self._has_liftgate = has_liftgate
        self._doors_open = False

    @property
    def door_count(self):
        return self._door_count

    @property
    def has_liftgate(self):
        return self._has_liftgate

    def open_doors(self):
        """Open cargo doors."""
        self._doors_open = True
        return True

    def close_doors(self):
        """Close cargo doors."""
        self._doors_open = False
        return True

    def use_liftgate(self):
        """Use the liftgate. Doors must be open.

        Raises:
            InvalidCargoStateException: If there is no liftgate or doors are closed.
        """
        if not self._has_liftgate:
            raise InvalidCargoStateException(
                title=self.plate,
                state="no_liftgate",
                reason="This van has no liftgate",
            )
        if not self._doors_open:
            raise InvalidCargoStateException(
                title=self.plate,
                state="doors_closed",
                reason="Open the doors before using the liftgate",
            )
        return True
