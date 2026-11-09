from logistics_cargo.Cargo import Cargo


class FragileCargo(Cargo):
    """Cargo that needs careful handling."""

    PACKING_COST_PER_KG = 2.0

    def __init__(
        self,
        weight: float,
        volume: float,
        origin,
        destination,
        packing_class: str,
        this_side_up: bool = True,
        min_insurance: float = 0.0,
        declared_value: float = 0.0,
    ):
        super().__init__(weight, volume, origin, destination, declared_value)
        if not packing_class:
            raise ValueError("Packing class must not be empty")
        if min_insurance < 0:
            raise ValueError(f"Min insurance must be non-negative, got {min_insurance}")
        self._packing_class = packing_class
        self._this_side_up = this_side_up
        self._min_insurance = min_insurance
        self._has_label = False

    @property
    def packing_class(self):
        return self._packing_class

    @property
    def this_side_up(self):
        return self._this_side_up

    @property
    def min_insurance(self):
        return self._min_insurance

    def require_label(self):
        """Attach a fragile-handling label."""
        self._has_label = True
        return True

    def check_orientation(self) -> bool:
        """Return True if the 'this side up' flag is set."""
        return self._this_side_up

    def estimate_packing(self) -> float:
        """Estimate packing cost from weight."""
        return FragileCargo.PACKING_COST_PER_KG * self.weight
