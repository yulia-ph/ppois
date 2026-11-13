from datetime import date

from exceptions.InvalidCargoStateException import InvalidCargoStateException


class Contract:
    """A signed commercial contract."""

    def __init__(self, parties, terms: str, amount: float, valid_until: date):
        if not terms:
            raise ValueError("Terms must not be empty")
        if amount < 0:
            raise ValueError(f"Amount must be non-negative, got {amount}")
        if valid_until is None:
            raise ValueError("Valid-until date must not be None")
        self._parties = list(parties) if parties else []
        self._terms = terms
        self._amount = amount
        self._is_signed = False
        self._signed_date = None
        self._valid_until = valid_until

    @property
    def parties(self):
        return list(self._parties)

    @property
    def terms(self):
        return self._terms

    @property
    def amount(self):
        return self._amount

    @property
    def is_signed(self):
        return self._is_signed

    @property
    def signed_date(self):
        return self._signed_date

    @property
    def valid_until(self):
        return self._valid_until

    def add_party(self, party: str):
        """Add a party before signing."""
        if not party:
            raise ValueError("Party name must not be empty")
        if self._is_signed:
            raise InvalidCargoStateException(
                title="contract",
                state="signed",
                reason="Cannot add parties to a signed contract",
            )
        if party in self._parties:
            raise ValueError("Party is already listed")
        self._parties.append(party)
        return True

    def sign(self):
        """Sign the contract. Needs at least one party."""
        if self._is_signed:
            raise InvalidCargoStateException(
                title="contract",
                state="signed",
                reason="Contract is already signed",
            )
        if not self._parties:
            raise ValueError("Cannot sign a contract with no parties")
        self._is_signed = True
        self._signed_date = date.today()
        return True

    def terminate(self):
        """Terminate a signed contract."""
        if not self._is_signed:
            raise InvalidCargoStateException(
                title="contract",
                state="draft",
                reason="Cannot terminate an unsigned contract",
            )
        self._is_signed = False
        return True

    def is_active(self, on_date: date = None) -> bool:
        """True if signed and not past valid_until."""
        day = on_date or date.today()
        return self._is_signed and day <= self._valid_until

    def change_amount(self, new_amount: float):
        """Change amount before signing."""
        if new_amount < 0:
            raise ValueError(f"Amount must be non-negative, got {new_amount}")
        if self._is_signed:
            raise InvalidCargoStateException(
                title="contract",
                state="signed",
                reason="Cannot change amount of a signed contract",
            )
        self._amount = new_amount
        return True
