from exceptions.HazardousRestrictionException import HazardousRestrictionException
from exceptions.InvalidCargoStateException import InvalidCargoStateException
from logistics_fleet.Vehicle import Vehicle


class Tanker(Vehicle):
    """A liquid tanker that must be cleaned between products."""

    LICENSE_CATEGORY = "C"

    def __init__(
        self,
        plate: str,
        vin: str,
        capacity_kg: float,
        volume_m3: float,
        tank_volume: float,
        chemical_class: str,
    ):
        super().__init__(plate, vin, capacity_kg, volume_m3)
        if tank_volume <= 0:
            raise ValueError(f"Tank volume must be positive, got {tank_volume}")
        if not chemical_class:
            raise ValueError("Chemical class must not be empty")
        self._tank_volume = tank_volume
        self._chemical_class = chemical_class
        self._is_cleaned = True
        self._loaded_volume = 0.0

    @property
    def tank_volume(self):
        return self._tank_volume

    @property
    def chemical_class(self):
        return self._chemical_class

    @property
    def is_cleaned(self):
        return self._is_cleaned

    def is_compatible(self, chemical_class: str) -> bool:
        """Return True if the tank may take this chemical class."""
        if not chemical_class:
            raise ValueError("Chemical class must not be empty")
        if self._is_cleaned:
            return True
        return chemical_class == self._chemical_class

    def load_liquid(self, volume: float, chemical_class: str):
        """Load liquid into the tank.

        Raises:
            HazardousRestrictionException: If the product is incompatible.
        """
        if volume <= 0:
            raise ValueError(f"Volume must be positive, got {volume}")
        if not self.is_compatible(chemical_class):
            raise HazardousRestrictionException(
                reason=f"Cannot mix {chemical_class} with {self._chemical_class}",
            )
        if self._loaded_volume + volume > self._tank_volume:
            raise InvalidCargoStateException(
                title=self.plate,
                state="tank_full",
                reason="Not enough tank volume",
            )
        self._chemical_class = chemical_class
        self._loaded_volume += volume
        self._is_cleaned = False
        return True

    def unload_liquid(self):
        """Empty the tank. It still needs cleaning afterwards."""
        if self._loaded_volume <= 0:
            raise InvalidCargoStateException(
                title=self.plate,
                state="empty",
                reason="Tank is already empty",
            )
        self._loaded_volume = 0.0
        return True

    def clean_tank(self):
        """Clean the tank so it can take another product."""
        if self._loaded_volume > 0:
            raise InvalidCargoStateException(
                title=self.plate,
                state="loaded",
                reason="Unload the tank before cleaning",
            )
        self._is_cleaned = True
        return True
