import pytest

from exceptions.InvalidCargoStateException import InvalidCargoStateException
from logistics_orders.Invoice import Invoice
from logistics_orders.Payment import Payment


class TestInvoice:
    def test_invoice(self):
        inv = Invoice(50, "Acme")
        inv.issue()
        inv.change_amount(40)
        pay = Payment(40, Payment.METHOD_CARD)
        inv.pay(pay)
        assert inv.is_paid
        inv2 = Invoice(10, "Acme")
        inv2.cancel()
        with pytest.raises(InvalidCargoStateException):
            inv2.pay(Payment(10, Payment.METHOD_CARD))
        with pytest.raises(ValueError):
            Invoice(0, "A")
        with pytest.raises(ValueError):
            Invoice(1, "")
        inv3 = Invoice(5, "A")
        with pytest.raises(ValueError):
            inv3.pay(None)
        with pytest.raises(ValueError):
            inv3.pay(Payment(1, Payment.METHOD_CARD))
        with pytest.raises(ValueError):
            inv3.change_amount(0)
        inv3.pay(Payment(5, Payment.METHOD_CARD))
        with pytest.raises(InvalidCargoStateException):
            inv3.issue()
        with pytest.raises(InvalidCargoStateException):
            inv3.cancel()
        with pytest.raises(InvalidCargoStateException):
            inv3.change_amount(2)
