from datetime import date

from exceptions.InvalidExhibitStateException import InvalidExhibitStateException


class Invoice:
    """A bill the museum must pay (supplier, restorer, insurer, etc.).

    `payer` is who settles the bill — here that is the museum.
    Paying goes through `Administrator.pay_invoice`, which also spends
    museum budget.

    An invoice moves through states:

        ISSUED -> PAID
               |
               v
           CANCELLED

    The amount can only be changed while the invoice is in the ISSUED
    state. Payment must match the invoice amount exactly.
    """

    STATUS_ISSUED = "issued"
    STATUS_PAID = "paid"
    STATUS_CANCELLED = "cancelled"

    _counter = 0

    def __init__(self, amount: float, payer: str):
        """Initialize an invoice.

        Args:
            amount: Invoice amount. Must be positive.
            payer: Payer name. Must not be empty.

        Raises:
            ValueError: If amount is not positive or payer is empty.
        """
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

    @property
    def is_cancelled(self):
        return self._status == Invoice.STATUS_CANCELLED

    def pay(self, payment):
        """Pay the invoice.

        Args:
            payment: The payment. Must expose `.amount` and `.process()`.

        Raises:
            InvalidExhibitStateException: If the invoice is not issued.
            ValueError: If payment is None or its amount does not match.
            PaymentFailedException: Propagated from payment.process().
        """
        if self._status != Invoice.STATUS_ISSUED:
            raise InvalidExhibitStateException(
                exhibit_title=self._number,
                state=self._status,
                reason="Cannot pay an invoice that is not issued",
            )
        if payment is None:
            raise ValueError("Payment must not be None")
        if payment.amount != self._amount:
            raise ValueError(
                f"Payment amount {payment.amount} does not match "
                f"invoice amount {self._amount}"
            )
        payment.process()
        self._payment = payment
        self._status = Invoice.STATUS_PAID
        self._paid_date = date.today()
        return True

    def cancel(self):
        """Cancel the invoice.

        Raises:
            InvalidExhibitStateException: If the invoice is not issued.
        """
        if self._status != Invoice.STATUS_ISSUED:
            raise InvalidExhibitStateException(
                exhibit_title=self._number,
                state=self._status,
                reason="Cannot cancel an invoice that is not issued",
            )
        self._status = Invoice.STATUS_CANCELLED
        return True


    def change_amount(self, new_amount: float):
        """Change the invoice amount.

        Args:
            new_amount: New amount. Must be positive.

        Raises:
            ValueError: If new_amount is not positive.
            InvalidExhibitStateException: If the invoice is not issued.
        """
        if new_amount <= 0:
            raise ValueError(f"Amount must be positive, got {new_amount}")
        if self._status != Invoice.STATUS_ISSUED:
            raise InvalidExhibitStateException(
                exhibit_title=self._number,
                state=self._status,
                reason="Cannot change amount of a non-issued invoice",
            )
        self._amount = new_amount
        return True