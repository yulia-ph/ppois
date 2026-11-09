from datetime import date

from exceptions.InvalidCargoStateException import InvalidCargoStateException


class Invoice:
    """A bill the client pays the company."""

    STATUS_ISSUED = "issued"
    STATUS_PAID = "paid"
    STATUS_CANCELLED = "cancelled"

    _counter = 0

    def __init__(self, amount: float, payer: str):
        if amount <= 0:
            raise ValueError(f"Amount must be positive, got {amount}")
        if not payer:
            raise ValueError("Payer must not be empty")
        Invoice._counter += 1
        self._number = f"INV-{Invoice._counter:05d}"
        self._amount = amount
        self._payer = payer
        self._status = Invoice.STATUS_ISSUED
        self._issued_date = date.today()
        self._paid_date = None
        self._payment = None
        self._issued = False

    @property
    def number(self):
        return self._number

    @property
    def amount(self):
        return self._amount

    @property
    def payer(self):
        return self._payer

    @property
    def status(self):
        return self._status

    @property
    def issued_date(self):
        return self._issued_date

    @property
    def paid_date(self):
        return self._paid_date

    @property
    def payment(self):
        return self._payment

    @property
    def is_paid(self):
        return self._status == Invoice.STATUS_PAID

    def issue(self):
        """Mark the invoice as issued (idempotent after first call)."""
        if self._status != Invoice.STATUS_ISSUED:
            raise InvalidCargoStateException(
                title=self._number,
                state=self._status,
                reason="Cannot re-issue this invoice",
            )
        self._issued = True
        return True

    def pay(self, payment):
        """Process payment once and mark the invoice paid."""
        if self._status != Invoice.STATUS_ISSUED:
            raise InvalidCargoStateException(
                title=self._number,
                state=self._status,
                reason="Cannot pay an invoice that is not issued",
            )
        if payment is None:
            raise ValueError("Payment must not be None")
        if payment.amount != self._amount:
            raise ValueError(
                f"Payment amount {payment.amount} does not match invoice amount {self._amount}"
            )
        payment.process()
        self._payment = payment
        self._status = Invoice.STATUS_PAID
        self._paid_date = date.today()
        return True

    def cancel(self):
        """Cancel an issued unpaid invoice."""
        if self._status != Invoice.STATUS_ISSUED:
            raise InvalidCargoStateException(
                title=self._number,
                state=self._status,
                reason="Cannot cancel an invoice that is not issued",
            )
        self._status = Invoice.STATUS_CANCELLED
        return True

    def change_amount(self, new_amount: float):
        """Change amount while the invoice is still issued."""
        if new_amount <= 0:
            raise ValueError(f"Amount must be positive, got {new_amount}")
        if self._status != Invoice.STATUS_ISSUED:
            raise InvalidCargoStateException(
                title=self._number,
                state=self._status,
                reason="Cannot change amount of a non-issued invoice",
            )
        self._amount = new_amount
        return True
