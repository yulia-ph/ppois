import pytest

from exceptions.InvalidCargoStateException import InvalidCargoStateException
from exceptions.PaymentFailedException import PaymentFailedException
from logistics_orders.Payment import Payment


class TestPayment:
    def test_payment_once(self):
        p = Payment(10, Payment.METHOD_CARD)
        p.process()
        assert p.verify()
        with pytest.raises(InvalidCargoStateException):
            p.process()
        p.refund()
        f = Payment(10, Payment.METHOD_CASH)
        with pytest.raises(PaymentFailedException):
            f.fail("no")
        with pytest.raises(PaymentFailedException):
            f.process()

    def test_payment_errors(self):
        with pytest.raises(ValueError):
            Payment(0, Payment.METHOD_CARD)
        with pytest.raises(ValueError):
            Payment(1, "bitcoin")
        p = Payment(1, Payment.METHOD_TRANSFER)
        with pytest.raises(InvalidCargoStateException):
            p.refund()
        p.process()
        with pytest.raises(InvalidCargoStateException):
            p.fail()
