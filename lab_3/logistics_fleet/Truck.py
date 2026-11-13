from exceptions.VehicleOverloadException import VehicleOverloadException
from logistics_fleet.Vehicle import Vehicle


class Truck(Vehicle):
    """A truck that can hitch a trailer."""

    LICENSE_CATEGORY = "C"

    def __init__(
        self,
        plate: str,
        vin: str,
        capacity_kg: float,
        volume_m3: float,
        axles: int,
        has_sleeper: bool = False,
    ):
        super().__init__(plate, vin, capacity_kg, volume_m3)
        if axles < 2:
            raise ValueError(f"Axles must be at least 2, got {axles}")
        self._axles = axles
        self._has_sleeper = has_sleeper
        self._attached_trailer = None

    @property
    def axles(self):
        return self._axles

    @property
    def has_sleeper(self):
        return self._has_sleeper

    @property
    def attached_trailer(self):
        return self._attached_trailer

    def can_take_trailer(self, trailer) -> bool:
        """Return True if this truck can hitch the trailer."""
        if trailer is None:
            raise ValueError("Trailer must not be None")
        if self._attached_trailer is not None:
            return False
        return not trailer.is_attached

    def hitch_trailer(self, trailer):
        """Attach a trailer.

        Raises:
            VehicleOverloadException: If the trailer is heavier than truck capacity.
        """
        if not self.can_take_trailer(trailer):
            raise ValueError("Cannot hitch this trailer")
        if trailer.capacity_kg > self._capacity_kg * 2:
            raise VehicleOverloadException(
                plate=self._plate,
                weight=trailer.capacity_kg,
                capacity=self._capacity_kg * 2,
            )
        trailer.attach(self)
        self._attached_trailer = trailer
        return True

    def unhitch(self):
        """Detach the current trailer."""
        if self._attached_trailer is None:
            raise ValueError("No trailer is attached")
        self._attached_trailer.detach()
        self._attached_trailer = None
        return True

    def axle_load(self) -> float:
        """Rough load per axle using truck capacity."""
        extra = self._attached_trailer.capacity_kg if self._attached_trailer else 0.0
        return (self._capacity_kg + extra) / self._axles
