from exceptions.HazardousRestrictionException import HazardousRestrictionException
from logistics_cargo.Cargo import Cargo


class HazardousCargo(Cargo):
    """Dangerous goods with a UN number and hazard class."""

    INCOMPATIBLE = {
        "1": {"3", "5"},
        "3": {"1"},
        "5": {"1"},
    }

    def __init__(
        self,
        weight: float,
        volume: float,
        origin,
        destination,
        un_number: str,
        hazard_class: str,
        requires_escort: bool = False,
        declared_value: float = 0.0,
    ):
        super().__init__(weight, volume, origin, destination, declared_value)
        if not un_number:
            raise ValueError("UN number must not be empty")
        if not hazard_class:
            raise ValueError("Hazard class must not be empty")
        self._un_number = un_number
        self._hazard_class = hazard_class
        self._requires_escort = requires_escort

    @property
    def un_number(self):
        return self._un_number

    @property
    def hazard_class(self):
        return self._hazard_class

    @property
    def requires_escort(self):
        return self._requires_escort

    def needs_permit(self) -> bool:
        """Return True if this cargo needs a checkpoint permit."""
        return self._requires_escort or self._hazard_class == "1"

    def require_escort(self):
        """Mark that an escort is required."""
        self._requires_escort = True
        return True

    def compatible_with(self, other) -> bool:
        """Return True if this cargo may travel with `other`.

        Raises:
            HazardousRestrictionException: If the classes cannot mix.
        """
        if other is None:
            raise ValueError("Other cargo must not be None")
        other_class = getattr(other, "hazard_class", None)
        if other_class is None:
            return True
        banned = HazardousCargo.INCOMPATIBLE.get(self._hazard_class, set())
        if other_class in banned:
            raise HazardousRestrictionException(
                reason=f"Class {self._hazard_class} cannot mix with {other_class}",
            )
        return True
