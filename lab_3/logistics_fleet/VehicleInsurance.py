from datetime import date, timedelta

from exceptions.InvalidCargoStateException import InvalidCargoStateException


class VehicleInsurance:
    """An insurance policy covering one vehicle."""

    STATUS_ACTIVE = "active"
    STATUS_CANCELLED = "cancelled"
    STATUS_CLAIMED = "claimed"

    def __init__(self, vehicle, company: str, amount: float, valid_until: date):
        if vehicle is None:
            raise ValueError("Vehicle must not be None")
        if not company:
            raise ValueError("Company must not be empty")
        if amount <= 0:
            raise ValueError(f"Amount must be positive, got {amount}")
        if valid_until is None:
            raise ValueError("Valid-until date must not be None")
        self._vehicle = vehicle
        self._company = company
        self._amount = amount
        self._valid_until = valid_until
        self._policy_number = f"INS-{vehicle.plate}"
        self._status = VehicleInsurance.STATUS_ACTIVE

    @property
    def vehicle(self):
        return self._vehicle

    @property
    def company(self):
        return self._company

    @property
    def amount(self):
        return self._amount

    @property
    def valid_until(self):
        return self._valid_until

    @property
    def policy_number(self):
        return self._policy_number

    def is_active(self) -> bool:
        """Return True if the policy is active and not expired."""
        return (
            self._status == VehicleInsurance.STATUS_ACTIVE
            and self._valid_until >= date.today()
        )

    def renew(self, extra_days: int):
        """Extend the policy.

        Raises:
            InvalidCargoStateException: If the policy is cancelled.
        """
        if extra_days <= 0:
            raise ValueError(f"Extra days must be positive, got {extra_days}")
        if self._status == VehicleInsurance.STATUS_CANCELLED:
            raise InvalidCargoStateException(
                title=self._policy_number,
                state=self._status,
                reason="Cannot renew a cancelled policy",
            )
        self._valid_until = self._valid_until + timedelta(days=extra_days)
        self._status = VehicleInsurance.STATUS_ACTIVE
        return True

    def claim(self, claim_amount: float):
        """File a claim against the policy."""
        if claim_amount <= 0:
            raise ValueError(f"Claim amount must be positive, got {claim_amount}")
        if not self.is_active():
            raise InvalidCargoStateException(
                title=self._policy_number,
                state=self._status,
                reason="Policy is not active",
            )
        if claim_amount > self._amount:
            raise ValueError("Claim exceeds coverage")
        self._status = VehicleInsurance.STATUS_CLAIMED
        return True

    def cancel(self):
        """Cancel the policy."""
        if self._status == VehicleInsurance.STATUS_CANCELLED:
            raise InvalidCargoStateException(
                title=self._policy_number,
                state=self._status,
                reason="Policy is already cancelled",
            )
        self._status = VehicleInsurance.STATUS_CANCELLED
        return True
