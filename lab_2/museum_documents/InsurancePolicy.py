from datetime import date, timedelta

from exceptions.InvalidExhibitStateException import InvalidExhibitStateException


class InsurancePolicy:
    """An insurance policy for a museum exhibit.

    A policy has an insurance company, an insured amount, a validity
    date, and a policy number. Applying the policy to the exhibit
    (`insure_exhibit`) writes the insurance value and a back-reference
    into the exhibit itself.

    A canceled policy cannot be renewed, claimed, or have its amount
    changed.
    """

    DAYS_PER_MONTH = 30

    def __init__(self, exhibit, company: str, amount: float,
                 valid_until: date, policy_number: str):
        """Initialize an insurance policy.

        Args:
            exhibit: The insured exhibit. Must not be None.
            company: Insurance company name. Must not be empty.
            amount: Insured amount. Must be non-negative.
            valid_until: Last day of validity. Must not be None.
            policy_number: Unique policy number. Must not be empty.

        Raises:
            ValueError: If any argument is invalid.
        """
        if exhibit is None:
            raise ValueError("Exhibit must not be None")
        if not company:
            raise ValueError("Company must not be empty")
        if amount < 0:
            raise ValueError(f"Amount must be non-negative, got {amount}")
        if valid_until is None:
            raise ValueError("Valid-until date must not be None")
        if not policy_number:
            raise ValueError("Policy number must not be empty")

        self._exhibit = exhibit
        self._company = company
        self._amount = amount
        self._valid_until = valid_until
        self._policy_number = policy_number
        self._is_cancelled = False


    @property
    def exhibit(self):
        return self._exhibit

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

    @property
    def is_cancelled(self):
        return self._is_cancelled


    def insure_exhibit(self):
        """Apply this policy to the exhibit.

        Sets the exhibit's insurance value and attaches this policy to
        the exhibit.

        Raises:
            InvalidExhibitStateException: If the policy is canceled.
        """
        if self._is_cancelled:
            raise InvalidExhibitStateException(
                exhibit_title=self._policy_number,
                state="cancelled",
                reason="Cannot apply a cancelled policy",
            )
        self._exhibit.set_insurance_value(self._amount)
        self._exhibit.attach_insurance_policy(self)
        return True


    def is_active(self, today: date = None) -> bool:
        """Return True if the policy is in force on the given date."""
        if today is None:
            today = date.today()
        if self._is_cancelled:
            return False
        return today <= self._valid_until

    def renew(self, months: int):
        """Extend the policy by the given number of months.

        If the policy is still active, extends from its current end
        date. If expired, extends from today.

        Args:
            months: Number of months. Must be positive.

        Raises:
            ValueError: If months is not positive.
            InvalidExhibitStateException: If the policy is canceled.
        """
        if months <= 0:
            raise ValueError(f"Months must be positive, got {months}")
        if self._is_cancelled:
            raise InvalidExhibitStateException(
                exhibit_title=self._policy_number,
                state="cancelled",
                reason="Cannot renew a cancelled policy",
            )
        base = max(self._valid_until, date.today())
        self._valid_until = base + timedelta(days=InsurancePolicy.DAYS_PER_MONTH * months)
        return True


    def claim_insurance(self):
        """File an insurance claim.

        Raises:
            InvalidExhibitStateException: If the policy is canceled or
                not currently active.
        """
        if self._is_cancelled:
            raise InvalidExhibitStateException(
                exhibit_title=self._policy_number,
                state="cancelled",
                reason="Cannot claim on a cancelled policy",
            )
        if not self.is_active():
            raise InvalidExhibitStateException(
                exhibit_title=self._policy_number,
                state="expired",
                reason="Cannot claim on an expired policy",
            )
        return True


    def cancel(self):
        """Cancel the policy.

        Idempotent: cancelling an already canceled policy is not an error.
        """
        self._is_cancelled = True
        return True