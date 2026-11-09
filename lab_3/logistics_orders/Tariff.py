class Tariff:
    """Price list: per kilogram and per kilometre, with a minimum charge."""

    def __init__(self, name: str, per_kg: float, per_km: float, min_charge: float):
        if not name:
            raise ValueError("Tariff name must not be empty")
        if per_kg < 0 or per_km < 0 or min_charge < 0:
            raise ValueError("Tariff rates must be non-negative")
        self._name = name
        self._per_kg = per_kg
        self._per_km = per_km
        self._min_charge = min_charge
        self._is_active = True
        self._surcharge = 0.0

    @property
    def name(self):
        return self._name

    @property
    def per_kg(self):
        return self._per_kg

    @property
    def per_km(self):
        return self._per_km

    @property
    def min_charge(self):
        return self._min_charge

    @property
    def is_active(self):
        return self._is_active

    def is_applicable(self, cargo) -> bool:
        """A tariff applies when it is active and cargo is packed or created."""
        if cargo is None:
            raise ValueError("Cargo must not be None")
        return self._is_active and cargo.weight > 0

    def apply_surcharge(self, amount: float):
        """Add a flat surcharge."""
        if amount < 0:
            raise ValueError(f"Surcharge must be non-negative, got {amount}")
        if not self._is_active:
            raise ValueError("Cannot surcharge an inactive tariff")
        self._surcharge = amount
        return True

    def calculate_price(self, cargo, route) -> float:
        """Price from weight, distance and surcharge, at least min_charge."""
        if not self.is_applicable(cargo):
            raise ValueError("Tariff is not applicable")
        if route is None:
            raise ValueError("Route must not be None")
        raw = cargo.weight * self._per_kg + route.distance_km * self._per_km + self._surcharge
        return max(self._min_charge, raw)

    def deactivate(self):
        """Turn the tariff off."""
        self._is_active = False
        return True
