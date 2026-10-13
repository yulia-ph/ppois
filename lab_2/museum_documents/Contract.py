from datetime import date

from exceptions.InvalidExhibitStateException import InvalidExhibitStateException


class Contract:
    """A legal contract between the museum and one or more parties.

    A contract has a list of parties, terms, and an amount. It must be
    signed before it becomes binding and can be terminated afterward.
    A permit can optionally be issued under a signed contract (e.g. to
    allow a specific operation).

    Once signed, the parties and amount cannot be changed.
    """

    def __init__(self, parties, terms: str, amount: float):
        """Initialize a contract.

        Args:
            parties: An iterable of party names (they may be empty).
            terms: Free-form terms text. Must not be empty.
            amount: Contract amount. Must be non-negative.

        Raises:
            ValueError: If terms is empty or amount is negative.
        """
        if not terms:
            raise ValueError("Terms must not be empty")
        if amount < 0:
            raise ValueError(f"Amount must be non-negative, got {amount}")
        self._parties = list(parties) if parties else []
        self._terms = terms
        self._amount = amount
        self._is_signed = False
        self._signed_date = None
        self._permit_number = None


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
    def permit_number(self):
        return self._permit_number


    def add_party(self, party: str):
        """Add a party to the contract.

        Only allowed while the contract is not yet signed.

        Args:
            party: The party name. Must not be empty.

        Raises:
            ValueError: If party is empty or already present.
            InvalidExhibitStateException: If the contract is signed.
        """
        if not party:
            raise ValueError("Party name must not be empty")
        if self._is_signed:
            raise InvalidExhibitStateException(
                exhibit_title=self._terms,
                state="signed",
                reason="Cannot add a party to a signed contract",
            )
        if party in self._parties:
            raise ValueError(f"Party '{party}' is already in the contract")
        self._parties.append(party)
        return True


    def sign(self):
        """Sign the contract.

        Raises:
            InvalidExhibitStateException: If the contract is already
                signed, or has no parties.
        """
        if self._is_signed:
            raise InvalidExhibitStateException(
                exhibit_title=self._terms,
                state="signed",
                reason="Contract is already signed",
            )
        if not self._parties:
            raise InvalidExhibitStateException(
                exhibit_title=self._terms,
                state="no_parties",
                reason="Cannot sign a contract without parties",
            )
        self._is_signed = True
        self._signed_date = date.today()
        return True

    def terminate(self):
        """Terminate a signed contract.

        Raises:
            InvalidExhibitStateException: If the contract is not signed.
        """
        if not self._is_signed:
            raise InvalidExhibitStateException(
                exhibit_title=self._terms,
                state="not_signed",
                reason="Cannot terminate a contract that was not signed",
            )
        self._is_signed = False
        return True


    def issue_permit(self, number: str):
        """Issue a permit under this contract.

        Args:
            number: The permit number. Must not be empty.

        Raises:
            ValueError: If number is empty.
            InvalidExhibitStateException: If the contract is not signed.
        """
        if not number:
            raise ValueError("Permit number must not be empty")
        if not self._is_signed:
            raise InvalidExhibitStateException(
                exhibit_title=self._terms,
                state="not_signed",
                reason="Cannot issue a permit for an unsigned contract",
            )
        self._permit_number = number
        return True

    def revoke_permit(self):
        """Revoke the current permit.

        Idempotent: revoking when no permit exists is not an error.
        """
        self._permit_number = None
        return True


    def change_amount(self, new_amount: float):
        """Change the contract amount.

        Only allowed while the contract is not yet signed.

        Args:
            new_amount: The new amount. Must be non-negative.

        Raises:
            ValueError: If new_amount is negative.
            InvalidExhibitStateException: If the contract is signed.
        """
        if new_amount < 0:
            raise ValueError(f"Amount must be non-negative, got {new_amount}")
        if self._is_signed:
            raise InvalidExhibitStateException(
                exhibit_title=self._terms,
                state="signed",
                reason="Cannot change amount of a signed contract",
            )
        self._amount = new_amount
        return True