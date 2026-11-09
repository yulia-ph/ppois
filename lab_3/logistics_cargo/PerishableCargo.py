from datetime import date, timedelta

from logistics_cargo.Cargo import Cargo


class PerishableCargo(Cargo):
    """Cargo that must stay within a temperature range."""

    def __init__(
        self,
        weight: float,
        volume: float,
        origin,
        destination,
        temp_min: float,
        temp_max: float,
        expires_at: date,
        declared_value: float = 0.0,
    ):
        super().__init__(weight, volume, origin, destination, declared_value)
        if temp_min >= temp_max:
            raise ValueError("temp_min must be lower than temp_max")
        if expires_at is None:
            raise ValueError("Expiry date must not be None")
        self._temp_min = temp_min
        self._temp_max = temp_max
        self._expires_at = expires_at

    @property
    def temp_min(self):
        return self._temp_min

    @property
    def temp_max(self):
        return self._temp_max

    @property
    def expires_at(self):
        return self._expires_at

    def is_expired(self, on_date: date = None) -> bool:
        """Return True if the cargo has expired."""
        day = on_date or date.today()
        return day > self._expires_at

    def check_temperature(self, temperature: float) -> bool:
        """Return True if `temperature` is inside the allowed range."""
        return self._temp_min <= temperature <= self._temp_max

    def extend_shelf_life(self, days: int):
        """Push the expiry date forward."""
        if days <= 0:
            raise ValueError(f"Days must be positive, got {days}")
        self._expires_at = self._expires_at + timedelta(days=days)
        return True
